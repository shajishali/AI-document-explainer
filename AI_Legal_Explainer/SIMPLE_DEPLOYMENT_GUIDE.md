# 🚀 Simple AWS Deployment Guide

## Quick Start (5 Steps)

### Step 1: Install Prerequisites
```powershell
# Install AWS CLI
# Download from: https://aws.amazon.com/cli/

# Install Docker Desktop
# Download from: https://www.docker.com/products/docker-desktop/

# Install Terraform
# Download from: https://www.terraform.io/downloads.html
```

### Step 2: Configure AWS
```powershell
# Configure your AWS credentials
aws configure

# Enter your:
# - AWS Access Key ID
# - AWS Secret Access Key  
# - Default region (e.g., us-east-1)
# - Default output format (json)
```

### Step 3: Run Deployment Script
```powershell
# Navigate to your project directory
cd "AI Legal Doc Explainer\AI_Legal_Explainer"

# Run the automated deployment script
.\deploy_to_aws.ps1
```

### Step 4: Wait for Deployment
The script will:
- ✅ Build Docker image
- ✅ Deploy AWS infrastructure
- ✅ Push image to ECR
- ✅ Deploy application
- ✅ Show you the URL

### Step 5: Test Your App
- Open the URL provided by the script
- Test file uploads
- Test AI analysis features
- Verify user registration/login

## 🎯 What Gets Deployed

Your application will be deployed with:
- **ECS Fargate** - Serverless containers
- **RDS MySQL** - Managed database
- **ElastiCache Redis** - Caching layer
- **S3** - File storage
- **Application Load Balancer** - Traffic distribution
- **Auto-scaling** - Handles traffic spikes
- **CloudWatch** - Monitoring and logging

## 💰 Estimated Costs

**Development Environment:**
- ECS: ~$15-25/month
- RDS: ~$15-20/month  
- S3: ~$1-5/month
- **Total: ~$30-50/month**

**Production Environment:**
- ECS: ~$50-150/month
- RDS: ~$50-100/month
- S3: ~$5-20/month
- **Total: ~$100-270/month**

*Costs vary based on usage and region*

## 🚨 Important Notes

1. **Start with development environment first**
2. **Monitor your AWS costs** - Set up billing alerts
3. **Keep your AWS credentials secure**
4. **Test thoroughly before going to production**
5. **Backup your database regularly**

## 🔧 Troubleshooting

### Common Issues:

**"Docker build failed"**
- Ensure Docker Desktop is running
- Check you're in the correct directory

**"Terraform init failed"**
- Verify Terraform is installed
- Check internet connection

**"AWS credentials not found"**
- Run `aws configure` first
- Verify your access keys are correct

**"ECS service won't start"**
- Check CloudWatch logs
- Verify security group rules
- Ensure RDS is accessible

## 📞 Getting Help

If you encounter issues:
1. Check the detailed `DEPLOYMENT_CHECKLIST.md`
2. Review AWS service health dashboard
3. Check CloudWatch logs for errors
4. Verify all prerequisites are installed

## 🎉 Success!

Once deployed, you'll have:
- A production-ready AI Legal Document Explainer
- Auto-scaling infrastructure
- Professional monitoring and logging
- Secure, managed services
- Cost-optimized resources

---

**Ready to deploy? Run `.\deploy_to_aws.ps1` and follow the prompts! 🚀**
