# Technical Decisions Document (Refactored)

This document details the technical choices made during the tiny-service development.

### 1. Application: FastAPI and OpenTelemetry
- **Why?**: The service was developed with **FastAPI** for its high performance and automatic documentation. Instrumentation with **OpenTelemetry** was added as a example of APM configuration offering more observability.

### 2. Container: Docker Multi-Stage Build
- **Why?**: The **multi-stage build** strategy and execution with a **non-root user** remain an essential security and efficiency practice, regardless of the orchestrator.

### 3. Orchestration and Deployment: Kubernetes
- **Why?**:
    - *Kubernetes is the industry standard for container orchestration, offering self-healing, scalability, and a robust ecosystem. We use Kubernetes-native service discovery via DNS. Our application finds the SigNoz collector through its service address (`my-signoz-otel-collector.platform.svc.cluster.local`).

### 4. Observability Platform Deployment: Helm
- **Why?**: We install SigNoz on Kubernetes using its official **Helm Chart**. Installation via Helm is declarative and repeatable.

### 5. CI/CD: GitHub Actions with Trivy
- **Why?**: Code validation (tests) and image security scanning with **Trivy** remain critical steps in the pipeline, ensuring that only quality and secure artifacts are candidates for deployment.