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

## 1. System Architecture

### 1.1 Architecture Overview
DentiaPro implements a modern microservices architecture with the following key components:

- **API Gateway**: Nginx reverse proxy
- **Application Layer**: Django REST Framework (DRF)
- **Database Layer**: PostgreSQL with multi-tenancy support
- **Authentication**: JWT + OAuth2
- **Monitoring Stack**: Prometheus, Grafana, Sentry

### 1.2 Technology Stack
- **Backend Framework**: Django REST Framework
- **Database**: PostgreSQL
- **Web Server**: Nginx
- **Containerization**: Docker
- **CI/CD**: Jenkins
- **Monitoring**: Prometheus, Grafana
- **Error Tracking**: Sentry

## 2. Multi-Tenancy Implementation

### 2.1 Database Schema
The system implements a multi-tenant architecture with the following core models:

```python
# tenant/models.py
class Tenant(models.Model):
    name = models.CharField(max_length=100)
    domain_url = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

# users/models.py
class User(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
```

### 2.2 Core Entities
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

## 3. Authentication & Security

### 3.1 Authentication Flow
1. **JWT Implementation**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ],
}
```

### 3.2 Session Management
```python
# session/models.py
class Session(models.Model):
    session_id = models.UUIDField(primary_key=True)
    user_id = models.ForeignKey(User)
    token = models.CharField(max_length=500)
    expiration = models.DateTimeField()
    last_activity = models.DateTimeField(auto_now=True)
```

## 4. Core Services

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

## 5. Infrastructure Setup

### 5.1 Docker Configuration
```yaml
# docker-compose.yml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d

  backend:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/dentiapro
    depends_on:
      - db

  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

### 5.2 Nginx Configuration
```nginx
# nginx/conf.d/default.conf
server {
    listen 80;
    server_name _;

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 6. Development Guidelines

### 6.1 Code Structure
```plaintext
backend/
├── apps/
│   ├── appointments/
│   ├── users/
│   ├── tenants/

│   ├── medical_records/
│   ├── billing/
│   └── inventory/
├── core/
│   ├── middleware/
│   └── permissions/
└── config/
    └── settings/
```

### 6.2 API Standards
- Use HTTP methods appropriately (GET, POST, PUT, DELETE)
- Implement proper status codes
- Version APIs (e.g., /api/v1/)
- Use consistent naming conventions

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
        stage('Build') {
            steps {
                sh 'docker-compose build'
            }
        }
        stage('Test') {
            steps {
                sh 'docker-compose run backend python manage.py test'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }
}
```

### 8.2 Deployment Checklist
1. Database migrations
2. Static files collection
3. Environment variables setup
4. SSL certificate renewal
5. Backup verification
6. Service health checks