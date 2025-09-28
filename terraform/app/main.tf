provider "aws" {
  region = var.aws_region
}

terraform {
  backend "s3" {
    bucket = "soattc10-phase5-main-api"
    key    = "application/terraform.tfstate"
    region = "us-east-1"
  }
}

data "aws_eks_cluster_auth" "cluster" {
  name = var.cluster_name
}

provider "kubernetes" {
  host                   = data.terraform_remote_state.aws.outputs.eks_cluster_endpoint
  cluster_ca_certificate = base64decode(data.terraform_remote_state.aws.outputs.eks_cluster_ca)
  token                  = data.aws_eks_cluster_auth.cluster.token
}

resource "kubernetes_service" "main_api_lb" {
  metadata {
    name      = "main-api-lb"
    namespace = "default"
  }
  spec {
    selector = {
      app = "main-api"
    }
    type = "LoadBalancer"
    port {
      port        = 80
      target_port = 8000
    }
  }
}

resource "kubernetes_deployment" "main_api" {
  depends_on = [kubernetes_service.main_api_lb]
  metadata {
    name      = "main-api"
    namespace = "default"
    labels = {
      app = "main-api"
    }
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "main-api"
      }
    }
    template {
      metadata {
        labels = {
          app = "main-api"
        }
      }
      spec {
        container {
          name  = "main-api"
          image = local.application_image
          env{
            name = "AUTH_SERVICE_URL"
            value = "http://${data.terraform_remote_state.auth.outputs.auth_app_lb_endpoint}"
          }
          env{
            name = "AUTH_SERVICE_X_API_KEY"
            value = var.auth_api_key
          }
          env {
            name  = "FRAME_EXTRACTOR_SERVICE_URL"
            value = "http://${data.terraform_remote_state.frames.outputs.frames_app_lb_endpoint}"
          }
          env{
            name = "FRAME_EXTRACTOR_SERVICE_X_API_KEY"
            value = var.frame_api_key
          }
          env {
            name  = "ZIPPER_SERVICE_URL"
            value = "http://${data.terraform_remote_state.zipper.outputs.zipper_app_lb_endpoint}"
          }
          env{
            name = "ZIPPER_SERVICE_X_API_KEY"
            value = var.zipper_api_key
          }
          env{
            name = "API_X_API_KEY"
            value = var.main_api_key
          }
          env{
            name = "CALLBACK_URL"
            value = "http://${kubernetes_service.main_api_lb.status[0].load_balancer[0].ingress[0].hostname}/api/v1/notification"
          }
          env{
            name = "MONGO_HOST"
            value = data.terraform_remote_state.mongo.outputs.mongo_host
          }
          env {
            name  = "MONGO_DB"
            value = data.terraform_remote_state.mongo.outputs.mongo_db
          }
          env {
            name  = "MONGO_USER"
            value = data.terraform_remote_state.mongo.outputs.mongo_user
          }
          env {
            name  = "MONGO_PASSWORD"
            value = data.terraform_remote_state.mongo.outputs.mongo_password
          }
          env {
            name  = "MONGO_PORT"
            value = 27017
          }
          env {
            name  = "MONGO_URI"
            value = data.terraform_remote_state.mongo.outputs.mongo_uri            
          }          
          env {
            name  = "AUTH_SOURCE"
            value = data.terraform_remote_state.mongo.outputs.mongo_db  # zipper_microservice
          }
          env {
            name  = "MONGO_CONTAINER_NAME"
            value = data.terraform_remote_state.mongo.outputs.mongo_host  # zipper-microservice-mongodb
          }
          env {
            name  = "AWS_ACCESS_KEY_ID"
            value = var.aws_access_key_id
          }
          env {
            name  = "AWS_SECRET_ACCESS_KEY"
            value = var.aws_secret_access_key
          }
          env {
            name  = "AWS_SESSION_TOKEN"
            value = var.aws_session_token
          }
          env {
            name  = "AWS_DEFAULT_REGION"
            value = "us-east-1"
          }
          env {
            name  = "LOG_LEVEL"
            value = "INFO"
          }
          env {
            name  = "SECRET_KEY"
            value = var.secret_key
          }
          env {
            name  = "EMAIL_SENDER_ADDRESS"
            value = var.email_sender_address
          }
          env {
            name  = "EMAIL_HOST"
            value = var.email_host
          }
          env {
            name  = "EMAIL_PORT"
            value = var.email_port
          }
          env {
            name  = "EMAIL_HOST_USER"
            value = var.email_host_user
          }
          env {
            name  = "EMAIL_HOST_PASSWORD"
            value = var.email_host_password
          }
          env {
            name  = "EMAIL_USE_TLS"
            value = true
          }
          env {
            name  = "EMAIL_USE_SSL"
            value = false
          }
          port {
            container_port = 8000
          }
        }
      }
    }
  }
}