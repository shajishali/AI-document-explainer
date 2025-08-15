# Variables for AI Legal Explainer AWS infrastructure

variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (development, staging, production)"
  type        = string
  default     = "development"
  
  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be one of: development, staging, production."
  }
}

# VPC Configuration
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones to use"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24"]
}

# S3 Configuration
variable "s3_bucket_name" {
  description = "Name of the S3 bucket for app storage"
  type        = string
  default     = "ai-legal-explainer-storage"
}

# Database Configuration
variable "database_name" {
  description = "Name of the database"
  type        = string
  default     = "ai_legal_explainer"
}

variable "database_username" {
  description = "Database master username"
  type        = string
  default     = "admin"
}

variable "database_password" {
  description = "Database master password"
  type        = string
  sensitive   = true
}

variable "rds_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "rds_allocated_storage" {
  description = "Initial allocated storage for RDS (GB)"
  type        = number
  default     = 20
}

variable "rds_max_allocated_storage" {
  description = "Maximum allocated storage for RDS (GB)"
  type        = number
  default     = 100
}

# Redis Configuration
variable "redis_node_type" {
  description = "ElastiCache node type"
  type        = string
  default     = "cache.t3.micro"
}

variable "redis_num_cache_nodes" {
  description = "Number of cache nodes in Redis cluster"
  type        = number
  default     = 1
}

# ECS Configuration
variable "ecs_task_cpu" {
  description = "CPU units for ECS task (1024 = 1 vCPU)"
  type        = number
  default     = 1024
}

variable "ecs_task_memory" {
  description = "Memory for ECS task (MB)"
  type        = number
  default     = 2048
}

variable "ecs_service_desired_count" {
  description = "Desired number of ECS tasks"
  type        = number
  default     = 2
}

variable "ecs_service_min_count" {
  description = "Minimum number of ECS tasks for auto-scaling"
  type        = number
  default     = 1
}

variable "ecs_service_max_count" {
  description = "Maximum number of ECS tasks for auto-scaling"
  type        = number
  default     = 10
}

# Tags
variable "common_tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default = {
    Project     = "AI-Legal-Explainer"
    ManagedBy   = "Terraform"
    Owner       = "DevOps Team"
  }
}

# Cost Optimization
variable "enable_cost_optimization" {
  description = "Enable cost optimization features"
  type        = bool
  default     = true
}

variable "use_spot_instances" {
  description = "Use Spot instances for cost optimization (if applicable)"
  type        = bool
  default     = false
}

# Monitoring
variable "enable_monitoring" {
  description = "Enable CloudWatch monitoring and alerting"
  type        = bool
  default     = true
}

variable "monitoring_retention_days" {
  description = "Number of days to retain CloudWatch logs"
  type        = number
  default     = 30
}

# Security
variable "enable_encryption" {
  description = "Enable encryption at rest for all resources"
  type        = bool
  default     = true
}

variable "enable_ssl" {
  description = "Enable SSL/TLS for load balancer"
  type        = bool
  default     = false
}

variable "ssl_certificate_arn" {
  description = "ARN of SSL certificate for HTTPS"
  type        = string
  default     = ""
}

# Backup and Recovery
variable "enable_backups" {
  description = "Enable automated backups"
  type        = bool
  default     = true
}

variable "backup_retention_days" {
  description = "Number of days to retain backups"
  type        = number
  default     = 7
}

# Performance
variable "enable_cdn" {
  description = "Enable CloudFront CDN for static files"
  type        = bool
  default     = false
}

variable "enable_auto_scaling" {
  description = "Enable auto-scaling for ECS service"
  type        = bool
  default     = true
}

variable "auto_scaling_target_cpu" {
  description = "Target CPU utilization for auto-scaling"
  type        = number
  default     = 70
}

# Development Overrides
variable "dev_mode" {
  description = "Enable development mode with reduced resources"
  type        = bool
  default     = false
}

locals {
  # Conditional values based on environment
  is_production = var.environment == "production"
  is_development = var.environment == "development"
  
  # Resource sizing based on environment
  rds_instance_class = var.dev_mode ? "db.t3.micro" : var.rds_instance_class
  ecs_task_cpu = var.dev_mode ? 512 : var.ecs_task_cpu
  ecs_task_memory = var.dev_mode ? 1024 : var.ecs_task_memory
  ecs_service_desired_count = var.dev_mode ? 1 : var.ecs_service_desired_count
  
  # Cost optimization for non-production
  enable_cost_optimization = var.is_production ? false : var.enable_cost_optimization
  use_spot_instances = var.is_production ? false : var.use_spot_instances
  
  # Enhanced security for production
  enable_encryption = var.is_production ? true : var.enable_encryption
  enable_ssl = var.is_production ? true : var.enable_ssl
  enable_monitoring = var.is_production ? true : var.enable_monitoring
  enable_backups = var.is_production ? true : var.enable_backups
  
  # Performance optimization for production
  enable_cdn = var.is_production ? true : var.enable_cdn
  enable_auto_scaling = var.is_production ? true : var.enable_auto_scaling
}
