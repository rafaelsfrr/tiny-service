# Tiny Service - Take-Home Challenge (Kubernetes Edition)

This repository contains a Python (FastAPI) service deployed to a local Kubernetes cluster (`kind`), with an observability stack (SigNoz) installed via Helm.

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
- [Helm](https://helm.sh/docs/intro/install/) (The package manager for Kubernetes)

## How to Run

### 1. Create the Local Kubernetes Cluster

```bash
kind create cluster --name tiny-service-cluster
```

### 2. Install SigNoz via Helm

We will install SigNoz in the `platform` namespace.

```bash
# Add the SigNoz Helm repository
helm repo add signoz [https://charts.signoz.io](https://charts.signoz.io)

# Update the repositories
helm repo update

# Install SigNoz (using my-signoz as the release name)
# This may take a few minutes to download and start all pods.
helm install my-signoz signoz/signoz -n platform --create-namespace
```

**Verify that the installation was successful:**
```bash
kubectl get pods -n platform
# Wait until all pods have a status of Running or Completed.
```

### 3. Build and Load the Application Image

Build the Docker image locally and load it into the `kind` cluster.

```bash
# Build the image
docker build -t tiny-api:latest .

# Load the image into the cluster
kind load docker-image tiny-api:latest --name tiny-service-cluster
```

### 4. Deploy the Application

Apply the `tiny-api` manifests:
```bash
kubectl apply -f kubernetes/
```

**Verify that the application is running:**
```bash
kubectl get pods
# You should see 2 pods from the tiny-api-deployment with a Running status.
```

### 5. Access the Services

We will use `kubectl port-forward` to access both SigNoz and our API.

**Terminal 1 - Access SigNoz:**
```bash
# The SigNoz frontend runs on the my-signoz-frontend service
kubectl port-forward svc/my-signoz -n platform 3341:8080 
# Now access http://localhost:3301 in your browser.
```

**Terminal 2 - Access the tiny-api:**
```bash
# Forwards to our API's service
kubectl port-forward svc/tiny-api-service 8080:80
```

### 6. Generate Traffic and View Traces

With the API port-forward active, generate some requests:
```bash
# Run in a new terminal
while true; do curl -s "http://localhost:8080/greet?name=K8s" > /dev/null; echo "Request sent."; sleep 2; done
```
Go to the SigNoz UI in your browser (`http://localhost:3301`), wait a minute or two, and you will see the `tiny-api-service` appear in the 'Services' tab with all the traces from your requests.

### 7. Cleanup

```bash
# Deletes the kind cluster and all resources
kind delete cluster --name tiny-service-cluster
```