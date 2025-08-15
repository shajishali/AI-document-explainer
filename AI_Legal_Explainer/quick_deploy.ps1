# Quick Deploy Script for AI Legal Explainer
# Assumes AWS CLI, Docker, and Terraform are already configured

param(
    [string]$Environment = "development",
    [string]$Region = "us-east-1",
    [string]$ProjectName = "ai-legal-explainer"
)

Write-Host "🚀 Quick Deploy: AI Legal Explainer" -ForegroundColor Green
Write-Host "Environment: $Environment | Region: $Region" -ForegroundColor Cyan

# Build Docker image
Write-Host "`n🐳 Building Docker image..." -ForegroundColor Yellow
docker build -t $ProjectName:latest .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}

# Deploy infrastructure
Write-Host "`n🏗️  Deploying infrastructure..." -ForegroundColor Yellow
Set-Location terraform

# Create terraform.tfvars if it doesn't exist
if (-not (Test-Path "terraform.tfvars")) {
    $tfvarsContent = @"
aws_region = "$Region"
environment = "$Environment"
database_password = "ChangeMe123!"
s3_bucket_name = "$ProjectName-storage-$(Get-Random -Minimum 1000 -Maximum 9999)"
dev_mode = true
"@
    $tfvarsContent | Out-File -FilePath "terraform.tfvars" -Encoding UTF8
}

# Deploy
terraform init
terraform apply -var-file="terraform.tfvars" -auto-approve

# Get outputs
$ecrUrl = terraform output -raw ecr_repository_url
$albDns = terraform output -raw alb_dns_name

# Push to ECR
Write-Host "`n📤 Pushing to ECR..." -ForegroundColor Yellow
aws ecr get-login-password --region $Region | docker login --username AWS --password-stdin $ecrUrl
docker tag $ProjectName:latest $ecrUrl:latest
docker push $ecrUrl:latest

# Deploy application
Write-Host "`n🚀 Deploying application..." -ForegroundColor Yellow
aws ecs update-service --cluster ai-legal-cluster --service ai-legal-service --force-new-deployment --region $Region
aws ecs wait services-stable --cluster ai-legal-cluster --services ai-legal-service --region $Region

Write-Host "`n🎉 Deployment Complete!" -ForegroundColor Green
Write-Host "URL: http://$albDns" -ForegroundColor Cyan

Set-Location ..
