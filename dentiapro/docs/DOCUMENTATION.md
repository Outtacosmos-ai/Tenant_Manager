# DentiaPro: Technical Documentation

## Table of Contents
1. [System Architecture](#1-system-architecture)
2. [Multi-Tenancy Implementation](#2-multi-tenancy-implementation)
3. [Authentication & Security](#3-authentication--security)
4. [Core Services](#4-core-services)
5. [Infrastructure Setup](#5-infrastructure-setup)
6. [Development Guidelines](#6-development-guidelines)
7. [Monitoring & Logging](#7-monitoring--logging)
8. [Deployment Process](#8-deployment-process)

--------------------------------------------------------------------------------

## 1. System Architecture

### 1.1 Architecture Overview
DentiaPro uses a **modular Django architecture** packaged with Docker, making it straightforward to deploy and scale. Major components:

- **Nginx**: Acts as a reverse proxy and entry point for HTTP requests.
- **Django + Django REST Framework**: Main application layer with multiple modular apps (appointments, billing, etc.).
- **PostgreSQL**: Primary database supporting multi-tenant data separation.
- **Jenkins (CI/CD)**: Automated pipeline for build, test, and deployment.
- **Observability (Optional)**: Prometheus & Grafana for metrics, Sentry for error tracking.

### 1.2 Technology Stack
- **Framework**: Django 4.x + Django Rest Framework (DRF)
- **Database**: PostgreSQL
- **Web Server**: Nginx
- **Containerization**: Docker & docker-compose
- **CI/CD**: Jenkins
- **Monitoring**: Prometheus, Grafana
- **Error Tracking**: Sentry (optional)

--------------------------------------------------------------------------------

## 2. Multi-Tenancy Implementation

> _If you use [django-tenants](https://github.com/django-tenants/django-tenants), you’ll have a `Tenant` model and schema-based approach. If you use a custom approach (one database with a `tenant_id` foreign key in each model), adapt as needed._

### 2.1 Database Schema
DentiaPro uses **PostgreSQL**. Each tenant’s data is separated either by:
1. **Schema-based** approach (`django-tenants`), or
2. **Tenant foreign key** in each model.

# Example foreign-key–based model:

```python
# apps/tenant/models.py
class Tenant(models.Model):
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# users/models.py
class User(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
```

### 2.2 Tenant Identification
Tenants are identified by **subdomains**. For example, `tenant1.dentiapro.com` is a tenant for the `tenant1` subdomain.
- **Subdomain** or **HTTP header** can be used to identify the tenant at runtime.
- A custom Django middleware or `django-tenants` router can switch schema/queries accordingly.

--------------------------------------------------------------------------------

## 3. Core Services & Applications
DentiaPro splits functionality across multiple Django apps under `backend/apps/.` Common modules include:

1. **Medical Records**
   - Patient information
   - Diagnosis details
   - Treatment plans
   - Historical data

2. **Appointments**
   - Scheduling
   - Doctor assignments
   - Status tracking
   - Patient details

3. **Billing**
   - Payment processing
   - Invoice generation
   - Payment status tracking
   - Due date management

4. **Inventory**
   - Stock management
   - Item tracking
   - Price management
   - Reorder levels

Other modules (e.g., `authentication`, `prescription`, `tenant`) may also exist depending on project needs.

--------------------------------------------------------------------------------

## 4. Authentication & Security

### 4.1 Authentication Flow
DentiaPro supports JWT-based or session-based authentication. Example DRF config:

1. **JWT Implementation**
```python
# config/settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # or OAuth2, SessionAuth, etc.
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### 4.2 Session Management
```python
# session/models.py
class Session(models.Model):
    session_id = models.UUIDField(primary_key=True)
    user_id = models.ForeignKey(User)
    token = models.CharField(max_length=500)
    expiration = models.DateTimeField()
    last_activity = models.DateTimeField(auto_now=True)
```
### 4.3 Permissions
- **DRF permissions** (e.g., `IsAuthenticated`, `IsAdminUser`) or custom permission classes for tenant-based checks.
- Optionally, a `TenantPermission` ensures objects belong to the current tenant.

--------------------------------------------------------------------------------

## 5. Core Services

### 4.1 Medical Records Service
```python
# medical_records/views.py
class MedicalRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated, TenantPermission]

    def get_queryset(self):
        return MedicalRecord.objects.filter(
            tenant_id=self.request.user.tenant_id
        )
```

### 4.2 Appointment Management
```python
# appointments/models.py
class Appointment(models.Model):
    tenant = models.ForeignKey(Tenant)
    patient_name = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20)
```

--------------------------------------------------------------------------------

## 5. Infrastructure Setup

### 5.1 Docker Configuration
#### 5.1.1 Docker Compose
Place `docker-compose.yml` in the repo root (`dentiapro/`):

```yaml
version: '3.9'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: dentiapro_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - db_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    environment:
      - DJANGO_SECRET_KEY=dev_secret_key
      - DB_NAME=dentiapro_db
      - DB_USER=postgres
      - DB_PASSWORD=postgres
      - DB_HOST=db
      - DB_PORT=5432
    depends_on:
      - db
    ports:
      - "8000:8000"

  nginx:
    image: nginx:latest
    depends_on:
      - web
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    ports:
      - "80:80"

volumes:
  db_data:
```

#### 5.1.2 Dockerfile
A basic `Dockerfile` in the same root:

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### 5.2 Nginx Configuration
In `nginx/nginx.conf`:

```nginx
upstream django {
    server web:8000;
}

server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 5.3 Jenkins Configuration
- Jenkins URL: http://localhost:8080
- Jenkins credentials: admin/admin
- Jenkins job: `dentiapro/`


--------------------------------------------------------------------------------

## 6. Development Guidelines

### 6.1 Code Structure
```plaintext
backend/
├── apps/
│   ├── appointments/
│   ├── authentication/
│   ├── billing/
│   ├── inventory/
│   ├── medical_records/
│   ├── prescription/
│   ├── tenant/
│   └── users/
├── config/
│   ├── settings.py (or a settings/ folder)
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── manage.py
└── requirements.txt
```

### 6.2 Local Setup
1. **Clone** the repo & `cd dentiapro/`.
2. **Virtual env**: `python -m venv .venv` & `source .venv/bin/activate`.
3. **Install deps**: `pip install -r backend/requirements.txt`.
4. **DB**: Use PostgreSQL or quick `sqlite3` for local dev.
5. **Migrate**: `python backend/manage.py migrate`.
6. **Run server**: `python backend/manage.py runserver`.

### 6.3 Docker-Based Setup
1. **install** Docker & docker-compose.
2. **Build/Run**: `docker-compose up --build`.
3. **Stop**: `docker-compose down`.
4. **Rebuild**: `docker-compose build --no-cache`.
5. **Run server**: `docker-compose run --rm web python manage.py runserver`.
6. **Migrate**: `docker-compose run --rm web python manage.py migrate`.
7. **Access** at http://localhost (Nginx on port 80).

--------------------------------------------------------------------------------

## 7. Monitoring & Logging

### 7.1 Prometheus Configuration
```yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'dentiapro'
    static_configs:
      - targets: ['backend:8000']
```

### 7.2 Grafana Dashboard
- System metrics visualization
- Custom dashboards for:
  - API performance
  - Error rates
  - User activity
  - Database performance

### 7.3 Sentry Integration
```python
# settings.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
    environment="production"
)
```

## 8. Deployment Process

### 8.1 Jenkins Pipeline
```groovy
// Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t youruser/dentiapro-web:latest .'
            }
        }
        stage('Test') {
            steps {
                sh 'docker-compose up -d db'
                sh 'sleep 10'
                sh 'docker-compose run --rm web python manage.py migrate'
                sh 'docker-compose run --rm web pytest --maxfail=1'
                sh 'docker-compose down'
            }
        }
        stage('Push') {
            steps {
                sh 'docker login -u $DOCKER_USER -p $DOCKER_PASSWORD'
                sh 'docker push youruser/dentiapro-web:latest'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deployment steps go here (e.g., docker-compose up on a remote server).'
            }
        }
    }
}
```

### 8.2 Deployment Checklist
1. **DB Migrations**: `python manage.py migrate` or docker-compose run web python manage.py migrate.
2. **Static Files**: `python manage.py collectstatic`.
3. Environment Variables: Validate secrets in .env or Jenkins credentials.