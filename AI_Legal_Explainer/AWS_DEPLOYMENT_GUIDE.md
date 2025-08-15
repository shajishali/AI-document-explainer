# 🚀 AWS Deployment Guide for AI Legal Explainer

This guide provides comprehensive instructions for deploying your AI Legal Doc Explainer application to AWS using modern cloud infrastructure.

## 🏗️ Architecture Overview

```
Internet → CloudFront → Application Load Balancer → ECS Fargate → Django App
                                    ↓
                              RDS MySQL + ElastiCache Redis
                                    ↓
                              S3 (Static/Media Files)
```

## 📋 Prerequisites

- AWS CLI installed and configured
- Docker installed locally
- Terraform (optional, for infrastructure as code)
- Domain name (optional, for production)

## 🚀 Deployment Options

### Option 1: AWS ECS Fargate (Recommended)
- **Pros**: Serverless, auto-scaling, managed
- **Cons**: Slightly more expensive
- **Best for**: Production workloads

### Option 2: EC2 with Docker
- **Pros**: More control, cheaper for consistent workloads
- **Cons**: More management overhead
- **Best for**: Development/testing

### Option 3: AWS App Runner
- **Pros**: Simplest deployment
- **Cons**: Limited customization
- **Best for**: Simple applications

## 🔧 Step-by-Step Deployment

### 1. Prepare Your Application

#### 1.1 Environment Configuration
Create a `.env.production` file:

```bash
# Django Settings
SECRET_KEY=your-super-secret-production-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Database (RDS)
DB_NAME=ai_legal_explainer
DB_USER=app_user
DB_PASSWORD=your-secure-password
DB_HOST=your-rds-endpoint.region.rds.amazonaws.com
DB_PORT=3306

# AWS Services
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-app-bucket
AWS_S3_REGION_NAME=us-east-1

# Redis (ElastiCache)
REDIS_URL=redis://your-redis-endpoint:6379/0
CELERY_BROKER_URL=redis://your-redis-endpoint:6379/0
CELERY_RESULT_BACKEND=redis://your-redis-endpoint:6379/0

# Email (SES)
EMAIL_HOST=email-smtp.us-east-1.amazonaws.com
EMAIL_HOST_USER=your-ses-user
EMAIL_HOST_PASSWORD=your-ses-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Google AI
GOOGLE_API_KEY=your-gemini-api-key
```

#### 1.2 Build Docker Image
```bash
# Build the production image
docker build -t ai-legal-explainer:latest .

# Test locally
docker run -p 8000:8000 --env-file .env.production ai-legal-explainer:latest
```

### 2. AWS Infrastructure Setup

#### 2.1 Create S3 Bucket for Static/Media Files
```bash
aws s3 mb s3://your-app-bucket
aws s3api put-bucket-versioning --bucket your-app-bucket --versioning-configuration Status=Enabled
aws s3api put-bucket-encryption --bucket your-app-bucket --server-side-encryption-configuration '{
    "Rules": [
        {
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "AES256"
            }
        }
    ]
}'
```

#### 2.2 Create RDS MySQL Instance
```bash
aws rds create-db-instance \
    --db-instance-identifier ai-legal-db \
    --db-instance-class db.t3.micro \
    --engine mysql \
    --master-username admin \
    --master-user-password your-password \
    --allocated-storage 20 \
    --storage-encrypted \
    --vpc-security-group-ids sg-xxxxxxxxx \
    --db-subnet-group-name your-subnet-group
```

#### 2.3 Create ElastiCache Redis Cluster
```bash
aws elasticache create-replication-group \
    --replication-group-id ai-legal-redis \
    --replication-group-description "Redis for AI Legal Explainer" \
    --node-type cache.t3.micro \
    --num-cache-clusters 1 \
    --engine redis \
    --cache-parameter-group-family redis7 \
    --vpc-security-group-ids sg-xxxxxxxxx \
    --subnet-group-name your-subnet-group
```

### 3. ECS Fargate Deployment

#### 3.1 Create ECR Repository
```bash
aws ecr create-repository --repository-name ai-legal-explainer

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com

# Tag and push image
docker tag ai-legal-explainer:latest your-account.dkr.ecr.us-east-1.amazonaws.com/ai-legal-explainer:latest
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/ai-legal-explainer:latest
```

#### 3.2 Create ECS Cluster
```bash
aws ecs create-cluster --cluster-name ai-legal-cluster
```

#### 3.3 Create Task Definition
Create `task-definition.json`:

```json
{
    "family": "ai-legal-explainer",
    "networkMode": "awsvpc",
    "requiresCompatibilities": ["FARGATE"],
    "cpu": "1024",
    "memory": "2048",
    "executionRoleArn": "arn:aws:iam::your-account:role/ecsTaskExecutionRole",
    "taskRoleArn": "arn:aws:iam::your-account:role/ecsTaskRole",
    "containerDefinitions": [
        {
            "name": "ai-legal-app",
            "image": "your-account.dkr.ecr.us-east-1.amazonaws.com/ai-legal-explainer:latest",
            "portMappings": [
                {
                    "containerPort": 8000,
                    "protocol": "tcp"
                }
            ],
            "environment": [
                {
                    "name": "DJANGO_SETTINGS_MODULE",
                    "value": "AI_Legal_Explainer.production_settings"
                }
            ],
            "secrets": [
                {
                    "name": "SECRET_KEY",
                    "valueFrom": "arn:aws:secretsmanager:us-east-1:your-account:secret:ai-legal-secret:SECRET_KEY::"
                },
                {
                    "name": "DB_PASSWORD",
                    "valueFrom": "arn:aws:secretsmanager:us-east-1:your-account:secret:ai-legal-secret:DB_PASSWORD::"
                }
            ],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/ai-legal-explainer",
                    "awslogs-region": "us-east-1",
                    "awslogs-stream-prefix": "ecs"
                }
            },
            "healthCheck": {
                "command": ["CMD-SHELL", "curl -f http://localhost:8000/health/ || exit 1"],
                "interval": 30,
                "timeout": 5,
                "retries": 3,
                "startPeriod": 60
            }
        }
    ]
}
```

#### 3.4 Create Service
```bash
aws ecs create-service \
    --cluster ai-legal-cluster \
    --service-name ai-legal-service \
    --task-definition ai-legal-explainer:1 \
    --desired-count 2 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxxxxxx,subnet-yyyyyyyyy],securityGroups=[sg-xxxxxxxxx],assignPublicIp=ENABLED}" \
    --load-balancer "targetGroupArn=arn:aws:elasticloadbalancing:us-east-1:your-account:targetgroup/ai-legal-tg,containerName=ai-legal-app,containerPort=8000"
```

### 4. Load Balancer and Auto Scaling

#### 4.1 Create Application Load Balancer
```bash
aws elbv2 create-load-balancer \
    --name ai-legal-alb \
    --subnets subnet-xxxxxxxxx subnet-yyyyyyyyy \
    --security-groups sg-xxxxxxxxx
```

#### 4.2 Create Target Group
```bash
aws elbv2 create-target-group \
    --name ai-legal-tg \
    --protocol HTTP \
    --port 8000 \
    --vpc-id vpc-xxxxxxxxx \
    --target-type ip \
    --health-check-path /health/ \
    --health-check-interval-seconds 30 \
    --healthy-threshold-count 2 \
    --unhealthy-threshold-count 3
```

#### 4.3 Create Listener
```bash
aws elbv2 create-listener \
    --load-balancer-arn arn:aws:elasticloadbalancing:us-east-1:your-account:loadbalancer/app/ai-legal-alb/xxxxxxxxx \
    --protocol HTTP \
    --port 80 \
    --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:us-east-1:your-account:targetgroup/ai-legal-tg
```

### 5. CloudFront Distribution (Optional)

#### 5.1 Create CloudFront Distribution
```bash
aws cloudfront create-distribution \
    --distribution-config file://cloudfront-config.json
```

Create `cloudfront-config.json`:

```json
{
    "CallerReference": "ai-legal-explainer-$(date +%s)",
    "Comment": "AI Legal Explainer CloudFront Distribution",
    "DefaultCacheBehavior": {
        "TargetOriginId": "ai-legal-alb",
        "ViewerProtocolPolicy": "redirect-to-https",
        "TrustedSigners": {
            "Enabled": false,
            "Quantity": 0
        },
        "ForwardedValues": {
            "QueryString": true,
            "Cookies": {
                "Forward": "all"
            }
        },
        "MinTTL": 0,
        "DefaultTTL": 86400,
        "MaxTTL": 31536000
    },
    "Origins": {
        "Quantity": 1,
        "Items": [
            {
                "Id": "ai-legal-alb",
                "DomainName": "your-alb-dns-name.us-east-1.elb.amazonaws.com",
                "CustomOriginConfig": {
                    "HTTPPort": 80,
                    "HTTPSPort": 443,
                    "OriginProtocolPolicy": "http-only"
                }
            }
        ]
    },
    "Enabled": true,
    "PriceClass": "PriceClass_100"
}
```

### 6. Domain and SSL (Optional)

#### 6.1 Request SSL Certificate
```bash
aws acm request-certificate \
    --domain-name yourdomain.com \
    --subject-alternative-names www.yourdomain.com \
    --validation-method DNS
```

#### 6.2 Update Route 53
```bash
aws route53 create-hosted-zone --name yourdomain.com --caller-reference $(date +%s)
```

### 7. Monitoring and Logging

#### 7.1 Create CloudWatch Dashboard
```bash
aws cloudwatch put-dashboard \
    --dashboard-name "AI-Legal-Explainer" \
    --dashboard-body file://dashboard.json
```

#### 7.2 Set up CloudWatch Alarms
```bash
# CPU Utilization Alarm
aws cloudwatch put-metric-alarm \
    --alarm-name "ai-legal-cpu-high" \
    --alarm-description "CPU utilization is high" \
    --metric-name CPUUtilization \
    --namespace AWS/ECS \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 2 \
    --alarm-actions arn:aws:sns:us-east-1:your-account:your-topic
```

### 8. Backup and Disaster Recovery

#### 8.1 RDS Automated Backups
```bash
aws rds modify-db-instance \
    --db-instance-identifier ai-legal-db \
    --backup-retention-period 7 \
    --preferred-backup-window "02:00-03:00" \
    --preferred-maintenance-window "sun:03:00-sun:04:00"
```

#### 8.2 S3 Lifecycle Policy
```bash
aws s3api put-bucket-lifecycle-configuration \
    --bucket your-app-bucket \
    --lifecycle-configuration file://lifecycle.json
```

## 🔒 Security Best Practices

### 1. IAM Roles and Policies
- Use least privilege principle
- Rotate access keys regularly
- Use IAM roles for ECS tasks

### 2. Network Security
- Use private subnets for databases
- Implement security groups with minimal access
- Use VPC endpoints for AWS services

### 3. Data Encryption
- Enable encryption at rest for RDS
- Use HTTPS for all communications
- Encrypt S3 objects

### 4. Secrets Management
- Use AWS Secrets Manager for sensitive data
- Never commit secrets to version control
- Rotate secrets regularly

## 📊 Cost Optimization

### 1. Instance Sizing
- Start with t3.micro for development
- Use CloudWatch metrics to right-size
- Consider Spot instances for non-critical workloads

### 2. Storage Optimization
- Use S3 lifecycle policies
- Enable S3 Intelligent Tiering
- Use RDS storage autoscaling

### 3. Monitoring Costs
- Set up billing alerts
- Use AWS Cost Explorer
- Monitor unused resources

## 🚀 Deployment Commands

### Quick Deploy Script
Create `deploy.sh`:

```bash
#!/bin/bash

# Build and push Docker image
docker build -t ai-legal-explainer:latest .
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker tag ai-legal-explainer:latest $AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/ai-legal-explainer:latest
docker push $AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/ai-legal-explainer:latest

# Update ECS service
aws ecs update-service --cluster ai-legal-cluster --service ai-legal-service --force-new-deployment

# Wait for deployment
aws ecs wait services-stable --cluster ai-legal-cluster --services ai-legal-service

echo "Deployment completed successfully!"
```

### Make it executable:
```bash
chmod +x deploy.sh
./deploy.sh
```

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. ECS Service Won't Start
- Check task definition for syntax errors
- Verify IAM roles have correct permissions
- Check security group rules

#### 2. Database Connection Issues
- Verify RDS security group allows ECS traffic
- Check database credentials in Secrets Manager
- Ensure RDS is in the correct VPC

#### 3. Static Files Not Loading
- Verify S3 bucket permissions
- Check CloudFront distribution settings
- Ensure static files are collected

#### 4. High Response Times
- Check CloudWatch metrics
- Verify auto-scaling policies
- Monitor database performance

## 📚 Additional Resources

- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [AWS RDS Documentation](https://docs.aws.amazon.com/rds/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)

## 🎯 Next Steps

1. **Start Small**: Begin with a single ECS service
2. **Monitor**: Set up comprehensive monitoring
3. **Scale**: Implement auto-scaling based on metrics
4. **Optimize**: Continuously optimize performance and costs
5. **Secure**: Implement additional security measures

---

**Happy Deploying! 🚀**

Your AI Legal Explainer will be running on AWS with enterprise-grade infrastructure, auto-scaling, and high availability.
