locals {
  use_mock = (terraform.workspace == "default" || terraform.workspace == "test")
}

data "terraform_remote_state" "mongo" {
  backend = local.use_mock ? "local" : "s3"
  config = local.use_mock ? {
    path = "${path.module}/../mock/mock_mongo_outputs.tfstate"
    } : {
    bucket = "soattc10-phase5-main-api"
    key    = "env:/${terraform.workspace}/database/terraform.tfstate"
    region = "us-east-1"
  }
}

data "terraform_remote_state" "aws" {
  backend = local.use_mock ? "local" : "s3"
  config = local.use_mock ? {
    path = "${path.module}/../mock/mock_eks_outputs.tfstate"
  } : {
    bucket = "soattc10-phase5-aws-infra"
    key    = "env:/${terraform.workspace}/aws-infra/terraform.tfstate"
    region = "us-east-1"
  }
}

data "terraform_remote_state" "auth" {
  backend = local.use_mock ? "local" : "s3"
  config = local.use_mock ? {
    path = "${path.module}/../mock/mock_auth_outputs.tfstate"
  } : {
    bucket = "soattc10-phase5-auth-service"
    key    = "env:/${terraform.workspace}/application/terraform.tfstate"
    region = "us-east-1"
  }
}

data "terraform_remote_state" "frames" {
  backend = local.use_mock ? "local" : "s3"
  config = local.use_mock ? {
    path = "${path.module}/../mock/mock_frame_outputs.tfstate"
  } : {
    bucket = "soattc10-phase5-frames-service"
    key    = "env:/${terraform.workspace}/application/terraform.tfstate"
    region = "us-east-1"
  }
}

data "terraform_remote_state" "zipper" {
  backend = local.use_mock ? "local" : "s3"
  config = local.use_mock ? {
    path = "${path.module}/../mock/mock_zipper_outputs.tfstate"
  } : {
    bucket = "soattc10-phase5-zipper-service"
    key    = "env:/${terraform.workspace}/application/terraform.tfstate"
    region = "us-east-1"
  }
}