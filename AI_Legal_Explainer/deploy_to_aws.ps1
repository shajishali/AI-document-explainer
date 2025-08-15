# AI Legal Explainer AWS Deployment Script for Windows
# Run this script in PowerShell with Administrator privileges

Write-Host "🚀 AI Legal Explainer AWS Deployment Script" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# Check prerequisites
Write-Host "`n📋 Checking Prerequisites..." -ForegroundColor Yellow

# Check if AWS CLI is installed
try {
    $awsVersion = aws --version 2>$null
    if ($awsVersion) {
        Write-Host "✅ AWS CLI found: $awsVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ AWS CLI not found. Please install it first." -ForegroundColor Red
        Write-Host "   Download from: https://aws.amazon.com/cli/" -ForegroundColor Cyan
        exit 1
    }
} catch {
    Write-Host "❌ AWS CLI not found. Please install it first." -ForegroundColor Red
    exit 1
}

# Check if Docker is installed
try {
    $dockerVersion = docker --version 2>$null
    if ($dockerVersion) {
        Write-Host "✅ Docker found: $dockerVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ Docker not found. Please install Docker Desktop first." -ForegroundColor Red
        Write-Host "   Download from: https://www.docker.com/products/docker-desktop/" -ForegroundColor Cyan
        exit 1
    }
} catch {
    Write-Host "❌ Docker not found. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if Terraform is installed
try {
    $terraformVersion = terraform --version 2>$null
    if ($terraformVersion) {
        Write-Host "✅ Terraform found: $terraformVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ Terraform not found. Please install it first." -ForegroundColor Red
        Write-Host "   Download from: https://www.terraform.io/downloads.html" -ForegroundColor Cyan
        exit 1
    }
} catch {
    Write-Host "❌ Terraform not found. Please install it first." -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ All prerequisites are satisfied!" -ForegroundColor Green

# Configuration
Write-Host "`n⚙️  Configuration Setup..." -ForegroundColor Yellow

# Get AWS configuration
Write-Host "Please configure your AWS credentials:" -ForegroundColor Cyan
Write-Host "1. Run: aws configure" -ForegroundColor White
Write-Host "2. Enter your AWS Access Key ID" -ForegroundColor White
Write-Host "3. Enter your AWS Secret Access Key" -ForegroundColor White
Write-Host "4. Enter your preferred region (e.g., us-east-1)" -ForegroundColor White
Write-Host "5. Enter your preferred output format (json)" -ForegroundColor White

$configureAWS = Read-Host "`nHave you configured AWS CLI? (y/n)"
if ($configureAWS -ne "y" -and $configureAWS -ne "Y") {
    Write-Host "Please run 'aws configure' first and then run this script again." -ForegroundColor Red
    exit 1
}

# Get project configuration
Write-Host "`n📝 Project Configuration:" -ForegroundColor Cyan
$projectName = Read-Host "Enter project name (default: ai-legal-explainer)" 
if (-not $projectName) { $projectName = "ai-legal-explainer" }

$environment = Read-Host "Enter environment (development/staging/production) (default: development)"
if (-not $environment) { $environment = "development" }

$awsRegion = Read-Host "Enter AWS region (default: us-east-1)"
if (-not $awsRegion) { $awsRegion = "us-east-1" }

$databasePassword = Read-Host "Enter database password (required)" -AsSecureString
if (-not $databasePassword) {
    Write-Host "Database password is required!" -ForegroundColor Red
    exit 1
}

# Convert secure string to plain text for Terraform
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($databasePassword)
$databasePasswordPlain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

Write-Host "`n✅ Configuration completed!" -ForegroundColor Green

# Create terraform.tfvars file
Write-Host "`n📁 Creating Terraform configuration..." -ForegroundColor Yellow
$tfvarsContent = @"
# Terraform variables for AI Legal Explainer
aws_region = "$awsRegion"
environment = "$environment"
project_name = "$projectName"

# Database Configuration
database_password = "$databasePasswordPlain"

# S3 Configuration
s3_bucket_name = "$projectName-storage-$(Get-Random -Minimum 1000 -Maximum 9999)"

# Development mode (reduces costs)
dev_mode = true

# Enable monitoring
enable_monitoring = true

# Enable auto-scaling
enable_auto_scaling = true
"@

$tfvarsContent | Out-File -FilePath "terraform/terraform.tfvars" -Encoding UTF8
Write-Host "✅ Created terraform/terraform.tfvars" -ForegroundColor Green

# Step 2: Build and Push Docker Image
Write-Host "`n🐳 Building and Pushing Docker Image..." -ForegroundColor Yellow

# Build Docker image
Write-Host "Building Docker image..." -ForegroundColor White
docker build -t $projectName:latest .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker image built successfully" -ForegroundColor Green

# Step 3: Deploy Infrastructure with Terraform
Write-Host "`n🏗️  Deploying AWS Infrastructure..." -ForegroundColor Yellow

# Navigate to terraform directory
Set-Location terraform

# Initialize Terraform
Write-Host "Initializing Terraform..." -ForegroundColor White
terraform init

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Terraform initialization failed!" -ForegroundColor Red
    exit 1
}

# Plan Terraform deployment
Write-Host "Planning Terraform deployment..." -ForegroundColor White
terraform plan -var-file="terraform.tfvars"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Terraform plan failed!" -ForegroundColor Red
    exit 1
}

# Confirm deployment
$confirmDeploy = Read-Host "`nDo you want to proceed with the deployment? (y/n)"
if ($confirmDeploy -ne "y" -and $confirmDeploy -ne "Y") {
    Write-Host "Deployment cancelled by user." -ForegroundColor Yellow
    exit 0
}

# Apply Terraform configuration
Write-Host "Applying Terraform configuration..." -ForegroundColor White
terraform apply -var-file="terraform.tfvars" -auto-approve

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Terraform deployment failed!" -ForegroundColor Red
    exit 1
}

# Get outputs
Write-Host "Getting deployment outputs..." -ForegroundColor White
$ecrUrl = terraform output -raw ecr_repository_url
$albDns = terraform output -raw alb_dns_name

Write-Host "✅ Infrastructure deployed successfully!" -ForegroundColor Green
Write-Host "ECR Repository: $ecrUrl" -ForegroundColor Cyan
Write-Host "Load Balancer: $albDns" -ForegroundColor Cyan

# Step 4: Push Docker Image to ECR
Write-Host "`n📤 Pushing Docker Image to ECR..." -ForegroundColor Yellow

# Get ECR login token
Write-Host "Logging into ECR..." -ForegroundColor White
aws ecr get-login-password --region $awsRegion | docker login --username AWS --password-stdin $ecrUrl

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ECR login failed!" -ForegroundColor Red
    exit 1
}

# Tag and push image
Write-Host "Tagging and pushing image..." -ForegroundColor White
docker tag $projectName:latest $ecrUrl:latest
docker push $ecrUrl:latest

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Image push failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker image pushed to ECR successfully" -ForegroundColor Green

# Step 5: Deploy Application
Write-Host "`n🚀 Deploying Application..." -ForegroundColor Yellow

# Force new deployment
Write-Host "Updating ECS service..." -ForegroundColor White
aws ecs update-service --cluster ai-legal-cluster --service ai-legal-service --force-new-deployment --region $awsRegion

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ECS service update failed!" -ForegroundColor Red
    exit 1
}

# Wait for deployment to complete
Write-Host "Waiting for deployment to complete..." -ForegroundColor White
aws ecs wait services-stable --cluster ai-legal-cluster --services ai-legal-service --region $awsRegion

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Deployment failed to stabilize!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Application deployed successfully!" -ForegroundColor Green

# Step 6: Final Status
Write-Host "`n🎉 Deployment Complete!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host "Your AI Legal Explainer is now running on AWS!" -ForegroundColor White
Write-Host "`n📱 Access your application:" -ForegroundColor Cyan
Write-Host "URL: http://$albDns" -ForegroundColor White
Write-Host "`n🔍 Monitor your deployment:" -ForegroundColor Cyan
Write-Host "ECS Console: https://console.aws.amazon.com/ecs/home?region=$awsRegion" -ForegroundColor White
Write-Host "CloudWatch: https://console.aws.amazon.com/cloudwatch/home?region=$awsRegion" -ForegroundColor White
Write-Host "`n💰 Cost Management:" -ForegroundColor Cyan
Write-Host "Cost Explorer: https://console.aws.amazon.com/cost-management/home?region=$awsRegion" -ForegroundColor White

# Return to original directory
Set-Location ..

Write-Host "`n📚 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Test your application at http://$albDns" -ForegroundColor White
Write-Host "2. Set up monitoring and alerting" -ForegroundColor White
Write-Host "3. Configure custom domain and SSL (optional)" -ForegroundColor White
Write-Host "4. Set up automated backups" -ForegroundColor White
Write-Host "5. Monitor costs and optimize resources" -ForegroundColor White

Write-Host "`n🎯 Happy Deploying! 🚀" -ForegroundColor Green
