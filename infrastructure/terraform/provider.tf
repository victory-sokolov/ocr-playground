terraform {
  required_version = ">= 1.9.0"
  required_providers {
    helm = {
      source  = "hashicorp/helm"
      version = ">= 3.0.0"
    }
  }
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}
provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}
