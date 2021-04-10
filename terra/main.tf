
terraform {
  backend "remote" {
    organization = "nesamani"

    workspaces {
      name = "gh-actions"
    }
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.63.0"
    }
  }
}
