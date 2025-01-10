# DentiaPro API Reference

## Authentication

### Register
- *URL*: /api/auth/register/
- *Method*: POST
- *Data Params*: username, password, email
- *Success Response*: 201 Created
- *Error Response*: 400 Bad Request

### Login
- *URL*: /api/auth/login/
- *Method*: POST
- *Data Params*: username, password
- *Success Response*: 200 OK
- *Error Response*: 401 Unauthorized

### Refresh Token
- *URL*: /api/auth/refresh/
- *Method*: POST
- *Data Params*: refresh
- *Success Response*: 200 OK
- *Error Response*: 401 Unauthorized

## Cabinets

### List Cabinets
- *URL*: /api/cabinets/
- *Method*: GET
- *Success Response*: 200 OK

### Create Cabinet
- *URL*: /api/cabinets/
- *Method*: POST
- *Data Params*: name, address, contact_number
- *Success Response*: 201 Created
- *Error Response*: 400 Bad Request

### Retrieve Cabinet
- *URL*: /api/cabinets/<id>/
- *Method*: GET
- *Success Response*: 200 OK
- *Error Response*: 404 Not Found

### Update Cabinet
- *URL*: /api/cabinets/<id>/
- *Method*: PUT
- *Data Params*: name, address, contact_number
- *Success Response*: 200 OK
- *Error Response*: 400 Bad Request

### Delete Cabinet
- *URL*: /api/cabinets/<id>/
- *Method*: DELETE
- *Success Response*: 204 No Content
- *Error Response*: 404 Not Found

## Patients

### List Patients
- *URL*: /api/patients/
- *Method*: GET
- *Success Response*: 200 OK

### Create Patient
- *URL*: /api/patients/
- *Method*: POST
- *Data Params*: name, birthdate, contact_number, email
- *Success Response*: 201 Created
- *Error Response*: 400 Bad Request

### Retrieve Patient
- *URL*: /api/patients/<id>/
- *Method*: GET
- *Success Response*: 200 OK
- *Error Response*: 404 Not Found

### Update Patient
- *URL*: /api/patients/<id>/
- *Method*: PUT
- *Data Params*: name, birthdate, contact_number, email
- *Success Response*: 200 OK
- *Error Response*: 400 Bad Request

### Delete Patient
- *URL*: /api/patients/<id>/
- *Method*: DELETE
- *Success Response*: 204 No Content
- *Error Response*: 404 Not Found

## Consultations

### List Consultations
- *URL*: /api/consultations/
- *Method*: GET
- *Success Response*: 200 OK

### Create Consultation
- *URL*: /api/consultations/
- *Method*: POST
- *Data Params*: patient, cabinet, date, diagnosis, treatment
- *Success Response*: 201 Created
- *Error Response*: 400 Bad Request

### Retrieve Consultation
- *URL*: /api/consultations/<id>/
- *Method*: GET
- *Success Response*: 200 OK
- *Error Response*: 404 Not Found

### Update Consultation
- *URL*: /api/consultations/<id>/
- *Method*: PUT
- *Data Params*: patient, cabinet, date, diagnosis, treatment
- *Success Response*: 200 OK
- *Error Response*: 400 Bad Request

### Delete Consultation
- *URL*: /api/consultations/<id>/
- *Method*: DELETE
- *Success Response*: 204 No Content
- *Error Response*: 404 Not Found

## Monitoring

### Prometheus Metrics
- *URL*: /metrics/
- *Method*: GET
- *Success Response*: 200 OK
- *Description*: Returns Prometheus-formatted metrics for the application

### Health Check
- *URL*: /health/
- *Method*: GET
- *Success Response*: 200 OK
- *Error Response*: 503 Service Unavailable
- *Description*: Returns the health status of the application

## Tenants

### List Tenants
- *URL*: /api/tenants/
- *Method*: GET
- *Success Response*: 200 OK
- *Error Response*: 403 Forbidden

### Create Tenant
- *URL*: /api/tenants/
- *Method*: POST
- *Data Params*: name, schema_name, domain_url
- *Success Response*: 201 Created
- *Error Response*: 400 Bad Request

### Retrieve Tenant
- *URL*: /api/tenants/<id>/
- *Method*: GET
- *Success Response*: 200 OK
- *Error Response*: 404 Not Found

### Update Tenant
- *URL*: /api/tenants/<id>/
- *Method*: PUT
- *Data Params*: name, schema_name, domain_url
- *Success Response*: 200 OK
- *Error Response*: 400 Bad Request

### Delete Tenant
- *URL*: /api/tenants/<id>/
- *Method*: DELETE
- *Success Response*: 204 No Content
- *Error Response*: 404 Not Found

Note: Access to tenant-related endpoints may be restricted to superusers or administrators.
