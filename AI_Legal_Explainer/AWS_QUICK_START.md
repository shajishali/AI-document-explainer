# 🚀 AWS Quick Start Guide

Get your AI Legal Explainer running on AWS in under 30 minutes!

## ⚡ Quick Deploy (Recommended)

### 1. Prerequisites (5 minutes)
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Configure AWS
aws configure
```

### 2. Set Environment Variables (2 minutes)
```bash
export DATABASE_PASSWORD="your-secure-password-here"
export AWS_REGION="us-east-1"
export ENVIRONMENT="development"
```

### 3. Deploy Everything (20 minutes)
```bash
# Make script executable
chmod +x deploy_to_aws.sh

# Run deployment
./deploy_to_aws.sh
```

**That's it!** 🎉 Your app will be running on AWS.

---

## 🔧 Manual Deployment (Step by Step)

### Option 1: ECS Fargate (Serverless)

#### 1. Create S3 Bucket
```bash
aws s3 mb s3://ai-legal-explainer-storage
aws s3api put-bucket-versioning --bucket ai-legal-explainer-storage --versioning-configuration Status=Enabled
```

#### 2. Create ECR Repository
```bash
aws ecr create-repository --repository-name ai-legal-explainer
```

#### 3. Build and Push Docker Image
```bash
# Build image
docker build -t ai-legal-explainer:latest .

# Get ECR login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag ai-legal-explainer:latest $(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-east-1.amazonaws.com/ai-legal-explainer:latest
docker push $(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-east-1.amazonaws.com/ai-legal-explainer:latest
```

#### 4. Create ECS Cluster
```bash
aws ecs create-cluster --cluster-name ai-legal-cluster
```

#### 5. Create Task Definition
```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

#### 6. Create Service
```bash
aws ecs create-service \
    --cluster ai-legal-cluster \
    --service-name ai-legal-service \
    --task-definition ai-legal-explainer:1 \
    --desired-count 2 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx],securityGroups=[sg-xxxxx],assignPublicIp=ENABLED}"
```

### Option 2: EC2 with Docker (More Control)

#### 1. Launch EC2 Instance
```bash
aws ec2 run-instances \
    --image-id ami-0c02fb55956c7d316 \
    --count 1 \
    --instance-type t3.medium \
    --key-name your-key-pair \
    --security-group-ids sg-xxxxx \
    --subnet-id subnet-xxxxx
```

#### 2. SSH and Install Docker
```bash
ssh -i your-key.pem ec2-user@your-instance-ip

# Install Docker
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user
```

#### 3. Deploy Application
```bash
# Pull and run
docker pull your-ecr-repo/ai-legal-explainer:latest
docker run -d -p 80:8000 your-ecr-repo/ai-legal-explainer:latest
```

---

## 🌐 Domain and SSL Setup

### 1. Request SSL Certificate
```bash
aws acm request-certificate \
    --domain-name yourdomain.com \
    --subject-alternative-names www.yourdomain.com \
    --validation-method DNS
```

### 2. Update Route 53
```bash
aws route53 create-hosted-zone --name yourdomain.com
```

### 3. Point Domain to Load Balancer
Update your DNS A record to point to the ALB DNS name.

---

## 📊 Monitoring Setup

### 1. CloudWatch Dashboard
```bash
aws cloudwatch put-dashboard \
    --dashboard-name "AI-Legal-Explainer" \
    --dashboard-body file://dashboard.json
```

### 2. Set Up Alarms
```bash
# CPU Alarm
aws cloudwatch put-metric-alarm \
    --alarm-name "ai-legal-cpu-high" \
    --alarm-description "CPU utilization is high" \
    --metric-name CPUUtilization \
    --namespace AWS/ECS \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 2
```

---

## 💰 Cost Optimization

### 1. Use Spot Instances (EC2)
```bash
aws ec2 run-instances \
    --image-id ami-0c02fb55956c7d316 \
    --count 1 \
    --instance-type t3.medium \
    --instance-market-options MarketType=spot,SpotOptions={MaxPrice=0.05}
```

### 2. Enable S3 Lifecycle
```bash
aws s3api put-bucket-lifecycle-configuration \
    --bucket ai-legal-explainer-storage \
    --lifecycle-configuration file://lifecycle.json
```

### 3. RDS Storage Autoscaling
```bash
aws rds modify-db-instance \
    --db-instance-identifier ai-legal-db \
    --max-allocated-storage 100
```

---

## 🔒 Security Checklist

- [ ] Enable encryption at rest
- [ ] Use security groups with minimal access
- [ ] Store secrets in AWS Secrets Manager
- [ ] Enable CloudTrail logging
- [ ] Use IAM roles instead of access keys
- [ ] Enable VPC Flow Logs
- [ ] Set up CloudWatch alarms for security events

---

## 🚨 Troubleshooting

### Common Issues

#### 1. ECS Service Won't Start
```bash
# Check task definition
aws ecs describe-task-definition --task-definition ai-legal-explainer

# Check service events
aws ecs describe-services --cluster ai-legal-cluster --services ai-legal-service
```

#### 2. Database Connection Issues
```bash
# Check RDS status
aws rds describe-db-instances --db-instance-identifier ai-legal-db

# Check security groups
aws ec2 describe-security-groups --group-ids sg-xxxxx
```

#### 3. Static Files Not Loading
```bash
# Check S3 bucket permissions
aws s3api get-bucket-policy --bucket ai-legal-explainer-storage

# Verify CloudFront distribution
aws cloudfront get-distribution --id E1234567890
```

---

## 📚 Next Steps

1. **Set up CI/CD pipeline** with GitHub Actions or AWS CodePipeline
2. **Implement auto-scaling** based on CloudWatch metrics
3. **Add CloudFront CDN** for global performance
4. **Set up backup and disaster recovery**
5. **Implement monitoring and alerting**
6. **Add SSL certificate and custom domain**

---

## 🆘 Need Help?

- **AWS Documentation**: [docs.aws.amazon.com](https://docs.aws.amazon.com/)
- **AWS Support**: [aws.amazon.com/support](https://aws.amazon.com/support/)
- **Community**: [AWS Forums](https://forums.aws.amazon.com/)

---

**Happy Deploying! 🚀**

Your AI Legal Explainer will be running on enterprise-grade AWS infrastructure with auto-scaling, monitoring, and high availability.
