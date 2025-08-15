# 🚀 AWS Deployment Checklist for AI Legal Explainer

## 📋 Pre-Deployment Checklist

### 1. Prerequisites Installation
- [ ] **AWS CLI** installed and configured
- [ ] **Docker Desktop** installed and running
- [ ] **Terraform** installed (version >= 1.0)
- [ ] **PowerShell** (for Windows users) or **Bash** (for Linux/Mac users)

### 2. AWS Account Setup
- [ ] AWS account created and active
- [ ] IAM user with appropriate permissions created
- [ ] Access Key ID and Secret Access Key obtained
- [ ] AWS CLI configured (`aws configure`)
- [ ] Sufficient AWS credits/budget for deployment

### 3. Project Preparation
- [ ] All code committed to version control
- [ ] Environment variables documented
- [ ] Database migrations tested locally
- [ ] Docker image builds successfully locally
- [ ] Production settings configured

## 🏗️ Infrastructure Deployment

### 4. Terraform Setup
- [ ] Navigate to `terraform/` directory
- [ ] Review `main.tf` and `variables.tf`
- [ ] Create `terraform.tfvars` with your values
- [ ] Run `terraform init`
- [ ] Run `terraform plan` to review changes
- [ ] Run `terraform apply` to deploy infrastructure

### 5. AWS Resources Created
- [ ] VPC with public/private subnets
- [ ] Security groups configured
- [ ] RDS MySQL instance running
- [ ] ElastiCache Redis cluster active
- [ ] S3 bucket for static/media files
- [ ] ECR repository created
- [ ] ECS cluster and service running
- [ ] Application Load Balancer active
- [ ] CloudWatch log groups configured

## 🐳 Application Deployment

### 6. Docker Image
- [ ] Build Docker image: `docker build -t ai-legal-explainer:latest .`
- [ ] Test image locally: `docker run -p 8000:8000 ai-legal-explainer:latest`
- [ ] Login to ECR: `aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ecr-url>`
- [ ] Tag image for ECR: `docker tag ai-legal-explainer:latest <ecr-url>:latest`
- [ ] Push to ECR: `docker push <ecr-url>:latest`

### 7. ECS Service Update
- [ ] Force new deployment: `aws ecs update-service --cluster ai-legal-cluster --service ai-legal-service --force-new-deployment`
- [ ] Wait for service stability: `aws ecs wait services-stable --cluster ai-legal-cluster --services ai-legal-service`
- [ ] Verify tasks are running: `aws ecs describe-services --cluster ai-legal-cluster --services ai-legal-service`

## 🔍 Post-Deployment Verification

### 8. Application Testing
- [ ] Load balancer DNS name obtained
- [ ] Application accessible via HTTP
- [ ] Health check endpoint responding (`/health/`)
- [ ] Database connection working
- [ ] File uploads working (S3 integration)
- [ ] AI services responding
- [ ] User authentication working

### 9. Performance & Monitoring
- [ ] CloudWatch metrics visible
- [ ] Application logs accessible
- [ ] Error rates within acceptable limits
- [ ] Response times satisfactory
- [ ] Auto-scaling policies configured
- [ ] Cost monitoring enabled

### 10. Security Verification
- [ ] Security groups properly configured
- [ ] RDS not publicly accessible
- [ ] S3 bucket access restricted
- [ ] HTTPS enabled (if SSL certificate configured)
- [ ] Secrets stored in AWS Secrets Manager
- [ ] IAM roles follow least privilege principle

## 🚨 Troubleshooting Common Issues

### ECS Service Won't Start
- [ ] Check task definition for syntax errors
- [ ] Verify IAM roles have correct permissions
- [ ] Check security group rules
- [ ] Review CloudWatch logs for errors
- [ ] Ensure RDS and Redis are accessible

### Database Connection Issues
- [ ] Verify RDS security group allows ECS traffic
- [ ] Check database credentials in environment variables
- [ ] Ensure RDS is in the correct VPC
- [ ] Test database connectivity from ECS task

### Static Files Not Loading
- [ ] Verify S3 bucket permissions
- [ ] Check static files collection in Docker build
- [ ] Ensure S3 bucket name is correct
- [ ] Verify CloudFront distribution (if enabled)

### High Response Times
- [ ] Check CloudWatch metrics for bottlenecks
- [ ] Verify auto-scaling policies
- [ ] Monitor database performance
- [ ] Check Redis connection and performance

## 📊 Cost Optimization

### 11. Resource Optimization
- [ ] Use appropriate instance sizes (start with t3.micro)
- [ ] Enable auto-scaling based on demand
- [ ] Set up billing alerts
- [ ] Monitor unused resources
- [ ] Use Spot instances for non-critical workloads (if applicable)

### 12. Storage Optimization
- [ ] S3 lifecycle policies configured
- [ ] RDS storage autoscaling enabled
- [ ] CloudWatch log retention set appropriately
- [ ] Backup retention periods optimized

## 🔄 Continuous Deployment

### 13. Update Process
- [ ] Code changes committed to repository
- [ ] New Docker image built and tested
- [ ] Image pushed to ECR
- [ ] ECS service updated with new image
- [ ] Deployment monitored for success
- [ ] Rollback plan ready if needed

### 14. Monitoring & Alerting
- [ ] CloudWatch alarms configured
- [ ] SNS notifications set up
- [ ] Performance baselines established
- [ ] Error tracking implemented
- [ ] User experience monitoring enabled

## 📚 Useful Commands

### Infrastructure Management
```bash
# View infrastructure status
terraform show

# Plan changes
terraform plan -var-file="terraform.tfvars"

# Apply changes
terraform apply -var-file="terraform.tfvars"

# Destroy infrastructure (be careful!)
terraform destroy -var-file="terraform.tfvars"
```

### ECS Management
```bash
# View service status
aws ecs describe-services --cluster ai-legal-cluster --services ai-legal-service

# View task logs
aws logs tail /ecs/ai-legal-explainer --follow

# Scale service
aws ecs update-service --cluster ai-legal-cluster --service ai-legal-service --desired-count 3
```

### Docker Management
```bash
# Build image
docker build -t ai-legal-explainer:latest .

# Test locally
docker run -p 8000:8000 ai-legal-explainer:latest

# View running containers
docker ps

# View container logs
docker logs <container-id>
```

## 🎯 Success Criteria

Your deployment is successful when:
- [ ] Application is accessible via the load balancer URL
- [ ] All core features work (upload, AI analysis, user management)
- [ ] Database operations are working correctly
- [ ] File storage is functioning (S3 integration)
- [ ] Monitoring and logging are operational
- [ ] Auto-scaling responds to load changes
- [ ] Costs are within expected budget
- [ ] Security best practices are implemented

## 🆘 Getting Help

If you encounter issues:
1. Check CloudWatch logs for error messages
2. Review AWS service health dashboard
3. Consult AWS documentation and forums
4. Check Terraform state and outputs
5. Verify all prerequisites are met
6. Review security group and IAM configurations

---

**Happy Deploying! 🚀**

Remember: Start with development environment first, then move to staging, and finally production.
