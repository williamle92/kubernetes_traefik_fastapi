# Hyperion - Backend API Project

A modern, production-ready backend API built with FastAPI and deployed on Kubernetes. This project demonstrates industry-standard practices for building scalable web applications with asynchronous task processing.

## 📚 Table of Contents

- [What is This Project?](#what-is-this-project)
- [Technology Stack Explained](#technology-stack-explained)
- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Key Concepts for Beginners](#key-concepts-for-beginners)
- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Running the Application](#running-the-application)
- [Database Migrations](#database-migrations)
- [Kubernetes Deployment](#kubernetes-deployment)
- [API Documentation](#api-documentation)

---

## What is This Project?

Hyperion is a backend API application that provides:
- **User Authentication & Management**: Register, login, and manage user accounts
- **RESTful API**: Clean, well-structured endpoints following REST principles
- **Background Task Processing**: Handle long-running tasks without blocking API requests
- **Database Management**: Persistent data storage with automatic migrations
- **Cloud-Native Deployment**: Production-ready Kubernetes configuration

This project serves as a template or learning resource for building modern web applications.

---

## Technology Stack Explained

### Core Application

**FastAPI** - The Web Framework
- A modern Python framework for building APIs
- Automatically generates interactive API documentation
- Fast performance with async/await support
- Built-in data validation using Pydantic

**SQLAlchemy** - Database Toolkit
- An ORM (Object-Relational Mapper) that lets you work with databases using Python objects instead of SQL
- Example: Instead of writing SQL queries, you write Python code like `User.query.filter_by(email="user@example.com")`

**Alembic** - Database Migration Tool
- Manages changes to your database schema over time
- Think of it as "version control for your database"
- Allows you to upgrade/downgrade database structure safely

**PostgreSQL** - The Database
- A powerful, open-source relational database
- Stores all your application data (users, etc.)
- Supports complex queries and transactions

### Background Processing

**Celery** - Task Queue
- Handles tasks that take a long time (sending emails, processing data, etc.)
- Runs tasks in the background so your API responds quickly
- Example: When a user signs up, the API responds immediately while Celery sends a welcome email in the background

**Redis** - Message Broker & Cache
- Acts as a messenger between your API and Celery workers
- Stores tasks in a queue until workers can process them
- Also used for caching to speed up your application

### Authentication & Security

**Python-JOSE** - JWT Token Handling
- Creates and validates JWT (JSON Web Tokens)
- JWTs are like secure "tickets" that prove a user is logged in
- Used for stateless authentication (no need to store sessions on the server)

**Passlib & Bcrypt** - Password Security
- Safely hashes (encrypts) passwords before storing them
- Even if someone steals your database, they can't read the passwords
- Industry-standard security practice

### Development & Deployment

**Docker** - Containerization
- Packages your application with all its dependencies
- Ensures it runs the same way everywhere (your laptop, server, cloud)
- Think of it as a "shipping container" for software

**Kubernetes (K8s)** - Container Orchestration
- Manages multiple containers running your application
- Automatically handles scaling, restarts, and load balancing
- Production-grade deployment solution

**Helm** - Kubernetes Package Manager
- Makes it easier to deploy and manage Kubernetes applications
- Uses templates to configure your deployment
- Think of it as "apt-get" or "npm" for Kubernetes

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        KUBERNETES CLUSTER                    │
│                                                              │
│  ┌────────────────────┐         ┌──────────────────────┐   │
│  │   Ingress/Traefik  │         │   ConfigMap/Secrets  │   │
│  │  (Load Balancer)   │         │   (Configuration)    │   │
│  └──────────┬─────────┘         └──────────────────────┘   │
│             │                                                │
│  ┌──────────▼─────────┐                                     │
│  │   API Pods (x3)    │◄────┐                              │
│  │   (FastAPI App)    │     │                              │
│  └──────────┬─────────┘     │                              │
│             │               │                               │
│             │          Environment                          │
│             │          Variables                            │
│             │                                                │
│  ┌──────────▼─────────┐     │                              │
│  │   PostgreSQL DB    │     │                              │
│  │   (Data Storage)   │     │                              │
│  └────────────────────┘     │                              │
│                              │                               │
│  ┌─────────────────────┐    │                              │
│  │  Worker Pods (x2)   │◄───┘                              │
│  │  (Celery Workers)   │                                    │
│  └──────────┬──────────┘                                    │
│             │                                                │
│  ┌──────────▼──────────┐                                    │
│  │       Redis         │                                    │
│  │  (Message Broker)   │                                    │
│  └─────────────────────┘                                    │
└─────────────────────────────────────────────────────────────┘

Request Flow:
1. User sends HTTP request → Ingress (Traefik)
2. Ingress routes to API Pod
3. API processes request using PostgreSQL
4. If background task needed → queued in Redis
5. Worker picks up task from Redis and processes it
```

**Why This Architecture?**

- **Multiple API Pods (3)**: If one crashes, others keep serving requests
- **Separate Worker Pods (2)**: Background tasks don't slow down API responses
- **Redis Queue**: Decouples API from workers, allowing independent scaling
- **PostgreSQL**: Reliable data persistence
- **Traefik Ingress**: Single entry point with HTTPS support

---

## Project Structure

```
backend/
├── api/                        # Main application code
│   └── backend/
│       ├── main.py            # FastAPI application entry point
│       ├── configs.py         # Configuration management
│       ├── models/            # Database models (SQLAlchemy)
│       │   ├── users.py       # User model and roles
│       │   └── base.py        # Base model class
│       ├── routers/           # API endpoints
│       │   ├── auth.py        # Login, register endpoints
│       │   └── users.py       # User management endpoints
│       ├── pydantic/          # Request/Response schemas
│       │   ├── auth.py        # Auth data validation
│       │   └── users.py       # User data validation
│       ├── dependencies/      # Shared dependencies
│       │   └── auth.py        # Authentication helpers
│       ├── worker/            # Background task processing
│       │   └── tasks.py       # Celery tasks
│       └── migrations/        # Database migrations (Alembic)
│
├── kubernetes/                # Kubernetes deployment configs
│   ├── hyperion/             # Helm chart for the application
│   │   ├── Chart.yaml        # Chart metadata
│   │   ├── values.yaml       # Configuration values
│   │   ├── configmap.yaml    # Non-sensitive config
│   │   └── templates/        # K8s resource templates
│   │       ├── deployment.yaml        # API pods
│   │       ├── worker-deployment.yaml # Worker pods
│   │       ├── service.yaml           # Internal networking
│   │       └── ingress.yaml           # External access
│   ├── redis/                # Redis configuration
│   └── traefik/              # Ingress controller config
│
├── Dockerfile                # Container image definition
├── pyproject.toml           # Python dependencies (Poetry)
├── alembic.ini              # Database migration config
├── .env                     # Environment variables (local)
└── README.md                # This file
```

---

## Key Concepts

### 1. **API (Application Programming Interface)**
An API is how different software applications talk to each other. This project provides a REST API - a set of URLs that respond with data.

Example:
- `GET /v1/api/users` - Get list of users
- `POST /v1/api/auth/login` - Log in a user

### 2. **Asynchronous Programming (async/await)**
FastAPI uses async code to handle multiple requests simultaneously without waiting for slow operations (like database queries) to complete.

```python
async def get_user():  # Can handle other requests while waiting
    user = await database.get_user()  # Wait for database
    return user
```

### 3. **ORM (Object-Relational Mapping)**
Instead of writing SQL, you work with Python objects:

```python
# Without ORM (raw SQL)
cursor.execute("SELECT * FROM users WHERE email = ?", email)

# With ORM (SQLAlchemy)
user = User.query.filter_by(email=email).first()
```

### 4. **Database Migrations**
When you change your database structure (add a column, create a table), migrations record these changes:

```bash
# Create a migration for changes
poetry run task generate-migrations

# Apply migrations to database
poetry run task commit-migrations
```

### 5. **Environment Variables**
Configuration that changes between environments (local, staging, production) is stored in `.env` files:

```
PG_HOST=localhost      # Database location
SECRET_KEY=your-secret # JWT signing key
```

### 6. **Containers & Pods**
- **Container**: Your app + dependencies packaged together (Docker)
- **Pod**: Smallest deployable unit in Kubernetes (can contain 1+ containers)
- **Deployment**: Manages multiple identical pods

### 7. **JWT (JSON Web Tokens)**
A secure way to verify a user's identity:

1. User logs in with username/password
2. Server creates a JWT token (cryptographically signed)
3. User sends this token with each request
4. Server verifies the token to identify the user

### 8. **Message Queue (Celery + Redis)**
When you have tasks that take a long time:

1. API receives request → immediately queues task in Redis → responds to user
2. Worker picks up task from Redis → processes it in background
3. User doesn't have to wait

---

## Prerequisites

Before you begin, ensure you have installed:

- **Python 3.11+**: [Download](https://www.python.org/downloads/)
- **Poetry**: Python dependency manager
  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```
- **Docker Desktop**: For containerization [Download](https://www.docker.com/products/docker-desktop/)
- **PostgreSQL**: Database (or use Docker)
- **Redis**: Message broker (or use Docker)
- **kubectl**: Kubernetes CLI (for deployment)
- **Helm**: Kubernetes package manager (for deployment)

---

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/williamle92/kubernetes_traefik_fastapi.git
cd backend
```

### 2. Install Dependencies

```bash
# Install Python dependencies
poetry install
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Database Configuration
PG_HOST=localhost
PG_USER=postgres
PG_PASSWORD=your_password
PG_DB=your_db_name
PG_PORT=5432

# Authentication
SECRET_KEY=your-super-secret-key-change-this
SALT=your-salt-value-change-this
ALGORITHM=HS256

# Redis Configuration
REDIS_HOST=localhost
REDIS_PASSWORD=
```

### 4. Start Required Services

**Option A: Using Docker Compose** (Recommended for beginners)
```bash
cd api
docker compose up -d postgres redis
```

**Option B: Install Locally**
- Install PostgreSQL and create a database named `hyperion`
- Install Redis and start it

### 5. Run Database Migrations

```bash
# Generate migration files (if schema changed)
poetry run task generate-migrations

# Apply migrations to create tables
poetry run task commit-migrations
```

---

## Running the Application

### Start the API Server

```bash
poetry run task app
```

The API will be available at: `http://localhost:8000`

### Start the Celery Worker (for background tasks)

In a separate terminal:

```bash
poetry run task worker
```

### Access API Documentation

FastAPI automatically generates interactive docs:

- **Swagger UI**: http://localhost:8000/swagger
- **ReDoc**: http://localhost:8000/docs

These allow you to test API endpoints directly in your browser!

---

## Database Migrations

Alembic manages your database schema changes:

### Create a New Migration

After modifying models in `api/backend/models/`:

```bash
poetry run task generate-migrations
```

This creates a new migration file in `api/backend/migrations/versions/`

### Apply Migrations

```bash
poetry run task commit-migrations
```

### Rollback Last Migration

```bash
poetry run task rollback-migrations
```

### How It Works

1. You change a model (e.g., add a field to `User`)
2. Generate migration → Alembic detects the change
3. Commit migration → Database is updated
4. All team members can apply the same migration to stay in sync

---

### Understanding the Deployment

- **API Deployment**: 3 replicas for high availability
- **Worker Deployment**: 2 replicas for background tasks
- **Redis**: Message broker for Celery
- **PostgreSQL**: Database (configure separately or use managed service)
- **Traefik**: Routes external traffic to your API
- **ConfigMap**: Non-sensitive configuration
- **Secrets**: Sensitive data (passwords, keys)

---


## Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Celery**: https://docs.celeryq.dev/
- **Kubernetes**: https://kubernetes.io/docs/home/
- **Helm**: https://helm.sh/docs/
- **Docker**: https://docs.docker.com/

---

## License

This project is for educational purposes.

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

---

**Questions?** Check the API docs at `/swagger` or open an issue on GitHub.
