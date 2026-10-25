# Containerized CI/CD Deployment Platform

A containerized Flask application with PostgreSQL, automated using **GitLab CI/CD, GitLab Runner, Docker, Docker-in-Docker, and a private container registry**.

The project demonstrates an end-to-end CI/CD workflow where application code is built into a Docker image, pushed to a private GitLab Container Registry, and automatically deployed using Docker Compose.

---

## Architecture

```text
                    Developer
                        |
                        | git push / git tag
                        v
                +----------------+
                | GitLab         |
                | Repository     |
                +-------+--------+
                        |
                        | Pipeline Trigger
                        v
                +----------------+
                | GitLab Runner  |
                +-------+--------+
                        |
                 Docker-in-Docker
                        |
                        v
                +----------------+
                | Docker Build   |
                | Flask Image    |
                +-------+--------+
                        |
                        | docker push
                        v
              +----------------------+
              | GitLab Container     |
              | Registry             |
              +----------+-----------+
                         |
                         | docker pull
                         v
              +----------------------+
              | Deployment Server    |
              |                      |
              |  +----------------+  |
              |  | Flask App      |  |
              |  | Container      |  |
              |  +-------+--------+  |
              |          |           |
              |          v           |
              |  +----------------+  |
              |  | PostgreSQL     |  |
              |  | Container      |  |
              |  +----------------+  |
              +----------------------+
```

---

## Tech Stack

| Technology | Purpose |
|---|---|
| **Python / Flask** | Backend web application |
| **PostgreSQL** | Relational database |
| **Docker** | Application containerization |
| **Docker Compose** | Multi-container application deployment |
| **GitLab CI/CD** | CI/CD pipeline automation |
| **GitLab Runner** | Pipeline job execution |
| **Docker-in-Docker** | Docker image builds inside CI |
| **GitLab Container Registry** | Private Docker image storage |
| **Git** | Source control and versioning |
| **Jenkins** | CI/CD pipeline configuration included in the project |

---

## Project Structure

```text
Pipeline-Test/
│
├── .gitlab-ci.yml
├── Dockerfile
├── docker-compose.yml
├── Jenkinsfile
├── app.py
├── index.html
├── init.sql
├── requirements.txt
└── README.md
```

### Important files

**`.gitlab-ci.yml`**

Defines the GitLab CI/CD pipeline with separate build and deployment stages.

**`Dockerfile`**

Defines how the Flask application is packaged into a Docker image.

**`docker-compose.yml`**

Defines the Flask application and PostgreSQL services and their configuration.

**`init.sql`**

Initializes the PostgreSQL database schema.

**`Jenkinsfile`**

Contains the Jenkins pipeline configuration used for CI/CD experimentation.

---

# CI/CD Pipeline

The GitLab pipeline consists of two primary stages:

```text
Build
  |
  v
Deploy
```

## 1. Build Stage

The build job runs using a Docker-based GitLab Runner.

Docker-in-Docker is used to provide a Docker daemon inside the CI environment.

The pipeline:

1. Authenticates with the GitLab Container Registry.
2. Determines the Docker image tag.
3. Builds the Flask application image.
4. Tags the image.
5. Pushes the image to the GitLab Container Registry.

Example workflow:

```bash
docker build -t $CI_REGISTRY_IMAGE:$IMAGE_TAG .
docker push $CI_REGISTRY_IMAGE:$IMAGE_TAG
```

The image tag is based on the Git commit tag when available, otherwise `latest` is used.

---

## 2. Deploy Stage

The deployment job runs on a Docker-enabled runner.

The pipeline:

```bash
docker-compose down
docker-compose pull
docker-compose up -d
```

This stops the existing application, pulls the required application image from the private registry, and starts the updated application stack.

---

# Docker Architecture

The application is deployed as multiple containers using Docker Compose.

```text
Docker Compose
│
├── Flask Application
│   ├── Port: 5000
│   └── Connects to PostgreSQL
│
└── PostgreSQL
    ├── Port: 5432
    └── Persistent Docker Volume
```

The Flask application communicates with PostgreSQL through the Docker Compose service name:

```text
db
```

The database connection is configured using:

```text
postgresql://postgres:postgres@db:5432/tasksdb
```

The PostgreSQL container uses a persistent Docker volume:

```text
pg_data
```

to preserve database data across container restarts.

---

# Image Versioning

The pipeline supports Git-tag-based Docker image versioning.

For example:

```text
Git tag
   |
   +-- ver0.1
   +-- ver0.2
   +-- ver0.3
```

A Git tag can be used as the Docker image tag:

```text
gitlab.spit.ac.in:5050/devops/pipeline-test:ver0.3
```

If no Git tag is available, the pipeline falls back to:

```text
latest
```

This allows different application versions to be stored and deployed independently.

---

# PostgreSQL

The PostgreSQL service uses:

```text
postgres:16-alpine
```

Database configuration:

```text
Database: tasksdb
User:     postgres
Port:     5432
```

The database is initialized using:

```text
init.sql
```

A Docker health check is also configured using:

```bash
pg_isready -U postgres
```

The Flask application waits for PostgreSQL to become healthy before starting.

---

# Running Locally

## Prerequisites

Install:

- Docker
- Docker Compose
- Git

Clone the repository:

```bash
git clone https://github.com/yasomani413/Pipeline-Test.git
cd Pipeline-Test
```

Start the application stack:

```bash
docker compose up -d
```

Check running containers:

```bash
docker ps
```

The application will be available at:

```text
http://localhost:5000
```

PostgreSQL will be exposed on:

```text
localhost:5432
```

To stop the application:

```bash
docker compose down
```

---

# CI/CD Workflow

The complete workflow is:

```text
1. Developer pushes code
          |
          v
2. GitLab repository updated
          |
          v
3. GitLab pipeline triggered
          |
          v
4. GitLab Runner executes build job
          |
          v
5. Docker-in-Docker builds application image
          |
          v
6. Image pushed to GitLab Container Registry
          |
          v
7. Deploy job starts
          |
          v
8. Deployment server pulls image
          |
          v
9. Docker Compose recreates application
          |
          v
10. Flask + PostgreSQL running
```

---

# Key DevOps Concepts Demonstrated

This project demonstrates practical experience with:

- CI/CD pipeline automation
- GitLab CI/CD
- GitLab Runner
- Docker containerization
- Docker-in-Docker
- Docker Compose
- Private container registries
- Docker image tagging
- Git-based versioning
- Automated deployment
- Multi-container application architecture
- PostgreSQL containerization
- Persistent Docker volumes
- Container health checks
- Linux-based deployment environments

---

# Future Improvements

Potential improvements to the project include:

- Add automated unit and integration testing
- Add SonarQube code-quality analysis
- Add vulnerability scanning for Docker images
- Add environment-specific deployments
- Introduce staging and production environments
- Implement deployment rollback
- Replace Docker Compose deployment with Kubernetes
- Add Prometheus and Grafana monitoring
- Add centralized logging
- Implement secrets management
- Add GitLab deployment environments
- Introduce blue-green or rolling deployments

---

## Author

**Yash Somani**

Computer Engineering | DevOps | Infrastructure

[GitHub](https://github.com/yasomani413)

[LinkedIn](https://www.linkedin.com/in/yash-somani-958216205/)
