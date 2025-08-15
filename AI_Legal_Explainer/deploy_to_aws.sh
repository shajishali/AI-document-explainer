#!/bin/bash

# 🚀 AI Legal Explainer AWS Deployment Script
# This script automates the complete deployment process to AWS

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="ai-legal-explainer"
AWS_REGION="${AWS_REGION:-us-east-1}"
ENVIRONMENT="${ENVIRONMENT:-development}"
ECR_REPOSITORY_NAME="${PROJECT_NAME}"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if AWS CLI is installed
    if ! command -v aws &> /dev/null; then
        log_error "AWS CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install it first."
        exit 1
    fi
    
    # Check if Terraform is installed (optional)
    if ! command -v terraform &> /dev/null; then
        log_warning "Terraform is not installed. Infrastructure deployment will be skipped."
        SKIP_TERRAFORM=true
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        log_error "AWS credentials are not configured. Please run 'aws configure' first."
        exit 1
    fi
    
    log_success "Prerequisites check completed"
}

get_aws_account_id() {
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    log_info "AWS Account ID: $AWS_ACCOUNT_ID"
}

create_ecr_repository() {
    log_info "Creating ECR repository..."
    
    if aws ecr describe-repositories --repository-names "$ECR_REPOSITORY_NAME" --region "$AWS_REGION" &> /dev/null; then
        log_info "ECR repository already exists"
    else
        aws ecr create-repository \
            --repository-name "$ECR_REPOSITORY_NAME" \
            --region "$AWS_REGION" \
            --image-scanning-configuration scanOnPush=true
        
        log_success "ECR repository created"
    fi
    
    ECR_REPOSITORY_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME"
    log_info "ECR Repository URI: $ECR_REPOSITORY_URI"
}

build_and_push_docker_image() {
    log_info "Building Docker image..."
    
    # Build the image
    docker build -t "$PROJECT_NAME:latest" .
    
    # Tag for ECR
    docker tag "$PROJECT_NAME:latest" "$ECR_REPOSITORY_URI:latest"
    
    # Get ECR login token
    log_info "Logging in to ECR..."
    aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$ECR_REPOSITORY_URI"
    
    # Push to ECR
    log_info "Pushing image to ECR..."
    docker push "$ECR_REPOSITORY_URI:latest"
    
    log_success "Docker image built and pushed successfully"
}

deploy_infrastructure() {
    if [ "$SKIP_TERRAFORM" = true ]; then
        log_warning "Skipping infrastructure deployment (Terraform not available)"
        return
    fi
    
    log_info "Deploying infrastructure with Terraform..."
    
    cd "$SCRIPT_DIR/terraform"
    
    # Initialize Terraform
    terraform init
    
    # Plan the deployment
    log_info "Planning Terraform deployment..."
    terraform plan -var="environment=$ENVIRONMENT" -var="database_password=$DATABASE_PASSWORD"
    
    # Ask for confirmation
    read -p "Do you want to proceed with the deployment? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_warning "Deployment cancelled by user"
        return
    fi
    
    # Apply the configuration
    log_info "Applying Terraform configuration..."
    terraform apply -var="environment=$ENVIRONMENT" -var="database_password=$DATABASE_PASSWORD" -auto-approve
    
    # Get outputs
    ALB_DNS_NAME=$(terraform output -raw alb_dns_name)
    ECR_REPO_URL=$(terraform output -raw ecr_repository_url)
    RDS_ENDPOINT=$(terraform output -raw rds_endpoint)
    REDIS_ENDPOINT=$(terraform output -raw redis_endpoint)
    S3_BUCKET=$(terraform output -raw s3_bucket_name)
    
    log_success "Infrastructure deployed successfully"
    
    cd "$SCRIPT_DIR"
}

deploy_application() {
    log_info "Deploying application to ECS..."
    
    # Update ECS service to force new deployment
    aws ecs update-service \
        --cluster "${PROJECT_NAME}-cluster" \
        --service "${PROJECT_NAME}-service" \
        --force-new-deployment \
        --region "$AWS_REGION"
    
    # Wait for service to be stable
    log_info "Waiting for service to stabilize..."
    aws ecs wait services-stable \
        --cluster "${PROJECT_NAME}-cluster" \
        --services "${PROJECT_NAME}-service" \
        --region "$AWS_REGION"
    
    log_success "Application deployed successfully"
}

setup_monitoring() {
    log_info "Setting up CloudWatch monitoring..."
    
    # Create CloudWatch dashboard
    DASHBOARD_CONFIG=$(cat <<EOF
{
    "widgets": [
        {
            "type": "metric",
            "x": 0,
            "y": 0,
            "width": 12,
            "height": 6,
            "properties": {
                "metrics": [
                    ["AWS/ECS", "CPUUtilization", "ServiceName", "${PROJECT_NAME}-service", "ClusterName", "${PROJECT_NAME}-cluster"]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "$AWS_REGION",
                "title": "ECS CPU Utilization"
            }
        },
        {
            "type": "metric",
            "x": 12,
            "y": 0,
            "width": 12,
            "height": 6,
            "properties": {
                "metrics": [
                    ["AWS/ECS", "MemoryUtilization", "ServiceName", "${PROJECT_NAME}-service", "ClusterName", "${PROJECT_NAME}-cluster"]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "$AWS_REGION",
                "title": "ECS Memory Utilization"
            }
        }
    ]
}
EOF
)
    
    aws cloudwatch put-dashboard \
        --dashboard-name "${PROJECT_NAME}-dashboard" \
        --dashboard-body "$DASHBOARD_CONFIG" \
        --region "$AWS_REGION"
    
    log_success "Monitoring dashboard created"
}

create_environment_file() {
    log_info "Creating production environment file..."
    
    cat > .env.production <<EOF
# Django Settings
SECRET_KEY=$(openssl rand -hex 32)
DEBUG=False
ALLOWED_HOSTS=${ALB_DNS_NAME:-localhost}
CORS_ALLOWED_ORIGINS=http://${ALB_DNS_NAME:-localhost},https://${ALB_DNS_NAME:-localhost}

# Database (RDS)
DB_NAME=ai_legal_explainer
DB_USER=admin
DB_PASSWORD=${DATABASE_PASSWORD}
DB_HOST=${RDS_ENDPOINT:-localhost}
DB_PORT=3306

# AWS Services
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
AWS_STORAGE_BUCKET_NAME=${S3_BUCKET:-ai-legal-explainer-storage}
AWS_S3_REGION_NAME=${AWS_REGION}

# Redis (ElastiCache)
REDIS_URL=redis://${REDIS_ENDPOINT:-localhost}:6379/0
CELERY_BROKER_URL=redis://${REDIS_ENDPOINT:-localhost}:6379/0
CELERY_RESULT_BACKEND=redis://${REDIS_ENDPOINT:-localhost}:6379/0

# Google AI
GOOGLE_API_KEY=${GOOGLE_API_KEY}
EOF
    
    log_success "Production environment file created"
}

run_health_check() {
    log_info "Running health check..."
    
    if [ -n "$ALB_DNS_NAME" ]; then
        HEALTH_CHECK_URL="http://$ALB_DNS_NAME/health/"
        
        # Wait for service to be ready
        log_info "Waiting for service to be ready..."
        for i in {1..30}; do
            if curl -f "$HEALTH_CHECK_URL" &> /dev/null; then
                log_success "Health check passed!"
                return 0
            fi
            log_info "Attempt $i/30: Service not ready yet..."
            sleep 10
        done
        
        log_error "Health check failed after 30 attempts"
        return 1
    else
        log_warning "Skipping health check (ALB DNS name not available)"
    fi
}

cleanup() {
    log_info "Cleaning up local resources..."
    
    # Remove local Docker images
    docker rmi "$PROJECT_NAME:latest" 2>/dev/null || true
    docker rmi "$ECR_REPOSITORY_URI:latest" 2>/dev/null || true
    
    log_success "Cleanup completed"
}

main() {
    log_info "Starting AI Legal Explainer AWS deployment..."
    log_info "Environment: $ENVIRONMENT"
    log_info "AWS Region: $AWS_REGION"
    
    # Check prerequisites
    check_prerequisites
    
    # Get AWS account ID
    get_aws_account_id
    
    # Create ECR repository
    create_ecr_repository
    
    # Build and push Docker image
    build_and_push_docker_image
    
    # Deploy infrastructure (if Terraform is available)
    deploy_infrastructure
    
    # Deploy application
    deploy_application
    
    # Setup monitoring
    setup_monitoring
    
    # Create environment file
    create_environment_file
    
    # Run health check
    run_health_check
    
    # Cleanup
    cleanup
    
    # Final output
    log_success "🎉 Deployment completed successfully!"
    echo
    echo "📊 Application Information:"
    echo "   Load Balancer: http://${ALB_DNS_NAME:-N/A}"
    echo "   ECR Repository: ${ECR_REPOSITORY_URI:-N/A}"
    echo "   RDS Endpoint: ${RDS_ENDPOINT:-N/A}"
    echo "   Redis Endpoint: ${REDIS_ENDPOINT:-N/A}"
    echo "   S3 Bucket: ${S3_BUCKET:-N/A}"
    echo
    echo "🔍 Monitoring:"
    echo "   CloudWatch Dashboard: https://${AWS_REGION}.console.aws.amazon.com/cloudwatch/home?region=${AWS_REGION}#dashboards:name=${PROJECT_NAME}-dashboard"
    echo
    echo "📚 Next Steps:"
    echo "   1. Update your DNS to point to the Load Balancer"
    echo "   2. Set up SSL certificate for HTTPS"
    echo "   3. Configure monitoring alerts"
    echo "   4. Set up backup and disaster recovery"
}

# Handle script interruption
trap 'log_error "Deployment interrupted"; exit 1' INT TERM

# Check if required environment variables are set
if [ -z "$DATABASE_PASSWORD" ]; then
    log_error "DATABASE_PASSWORD environment variable is required"
    echo "Please set it before running the script:"
    echo "export DATABASE_PASSWORD='your-secure-password'"
    exit 1
fi

# Run main function
main "$@"
