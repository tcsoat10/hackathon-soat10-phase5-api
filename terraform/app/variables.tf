variable "aws_region" {
  default = "us-east-1"
}

variable "cluster_name" {
  default = "hacka-soat10tc-cluster-eks"
}

variable "vpc_cidr_block" {
  default = ["172.31.0.0/16"]
}

variable "accessConfig" {
  default = "API_AND_CONFIG_MAP"
}

variable "node_name" {
  default = "my-nodes-group"
}

variable "policy_arn" {
  default = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
}

variable "instance_type" {
  default = "t3.small"
}

variable "mongo_password" {
  description = "Database user password"
  type        = string
}

variable "mongo_db" {
  default = "zipper_service"
}

variable "mongo_user" {
  description = "Database username"
  type        = string
}

variable "mongo_host" {
  type        = string
  default = ""
}

variable "mongo_port" {
  type        = string
  default = "27017"
}

variable "auth_api_key" {
  description = "API Key for Auth Microservice"
  type        = string
}
variable "frame_api_key" {
  description = "API Key for Frame Extractor Microservice"
  type        = string
}
variable "zipper_api_key" {
  description = "API Key for Zipper Microservice"
  type        = string
}
variable "main_api_key" {
  description = "API Key for Zipper Microservice"
  type        = string
}

variable "aws_access_key_id" {
  description = "AWS Access Key"
  type        = string
}

variable "aws_secret_access_key" {
  description = "AWS Secret Key"
  type        = string
}

variable "aws_session_token" {
  description = "AWS Session Token"
  type        = string
}

variable "aws_account_id" {}
variable "email_host_user" {
  type    = string
  default = "techchallengersoat10@gmail.com"
}
variable "email_host_password" {}
variable "email_port" {
  type    = number
  default = 587
}
variable "email_host" {
  type    = string
  default = "smtp.gmail.com"
}
variable "email_sender_address" {
  type    = string
  default = "SOAT 10 Hackathon <techchallengersoat10@gmail.com>"
}
variable "secret_key" {}
variable "callback_url" {}


variable "application_image" {
  description = "Docker image for the application"
  type        = string
  default     = ""
}

locals {
  application_image = "${var.aws_account_id}.dkr.ecr.us-east-1.amazonaws.com/soattc-main-api:latest"
}

