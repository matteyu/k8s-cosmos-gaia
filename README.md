# K8s Cosmos Gaia

## Prerequisites

Ensure you have the following tools installed:

- kubectl
- Helm
- Docker
- Terraform
- Python3

## Project Structure

The project is structured as follows:

```
project-root/
│
├── docker/             # Dockerfile for building Docker image
│   └── Dockerfile
│
├── k8s/                # Kubernetes manifest files
│   ├── gaia-service.yml
│   ├── gaia-servicemonitor.yml
│   └── gaia-statefulset.yml
│
└── terraform/           # Terraform files for managing AWS resources
│    ├── main.tf
│    ├── variables.tf
│    ├── outputs.tf
└── scripts/           # python cli for automating deployment actions
    ├── cli.py
    ├── utils.py
```

## Instructions

### Building and Running the Dockerfile Locally

1. **Build Docker Image:**

   ```bash
   cd docker/
   docker build -t gaia .
   ```

   Replace `gaia` with your preferred image name.

2. **Run Docker Container:**

   ```bash
   docker run gaia

   # to run remote, simply do "docker run ajail/gaia:17.2.0"
   ```

### Applying Kubernetes Manifest Files

1. **Apply Kubernetes Manifests:**

   ```bash
   cd k8s/
   kubectl apply -f gaia-statefulset.yml
   kubectl apply -f gaia-service.yml
   kubectl apply -f gaia-servicemonitor.yml
   ```

2. **Check Deployment Status:**

   ```bash
   kubectl get pods
   kubectl get services
   ```

   Ensure all pods are running and services are available.

### Deploying Resources with Terraform

1. **Initialize Terraform:**

   ```bash
   cd terraform/
   terraform init
   ```

2. **Plan and Apply Terraform Changes:**

   ```bash
   terraform plan
   terraform apply
   ```

   Follow the prompts to apply changes.

3. **Verify Resources:**

   ```bash
   terraform show
   ```

   Verify the resources created by Terraform.

### Automation Script
   ```bash
   python3 scripts/cli.py

   * follow the prompts
   ```