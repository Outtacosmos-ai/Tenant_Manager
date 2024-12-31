# DentiaPro - Tenant Manager

## Overview
DentiaPro is a SaaS platform designed specifically for dental clinics to efficiently manage both administrative and medical operations. It includes a wide range of features such as:
- Appointment scheduling
- Patient medical records management
- Billing and invoicing
- Inventory tracking
- Communication tools

The platform is built with a multitenancy architecture, ensuring each tenant (clinic) has a secure and isolated environment for their data.

---

## Features

### Administrative Features:
- **Appointment Management:** Schedule, reschedule, and manage appointments with ease.
- **Billing and Invoicing:** Generate invoices, track payments, and manage billing cycles.
- **Inventory Management:** Monitor stock levels and track supplies in real-time.

### Medical Features:
- **Patient Records:** Maintain detailed and secure medical histories for patients.
- **Treatment Plans:** Create and manage personalized treatment plans.
- **Reports:** Generate reports for analysis and decision-making.

---

## Installation and Setup

### Prerequisites
Ensure you have the following installed:
- **Python:** Version 3.10+
- **PostgreSQL:** Version 13+
- **Docker (Optional):** For containerized deployment

### Steps to Set Up Locally

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Outtacosmos-ai/Tenant_Manager.git
   cd dentiapro
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Database:**
   - Create a PostgreSQL database named `dentiapro`.
   - Update the `DATABASES` settings in `settings.py` with your database credentials.
   - Run migrations:
     ```bash
     python manage.py migrate
     ```

5. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

---

## API Endpoints

### Authentication
- **POST** `/api/auth/login`
  - Logs in a user and returns JWT tokens.

### Patient Management
- **POST** `/api/patients/`
  - Adds a new patient record.

### Appointments
- **GET** `/api/appointments/`
  - Retrieves a list of all appointments.

Refer to the [API documentation](./docs/api_documentation.md) for a full list of endpoints.

---

## Testing

DentiaPro includes unit tests to ensure reliability. We recommend using **pytest** to run the test suite.

### Run Tests
Activate the virtual environment and run:
```bash
pytest
```

---

## Deployment

### Using Docker
1. Build the Docker image:
   ```bash
   docker build -t dentiapro .
   ```
2. Start the application:
   ```bash
   docker-compose up -d
   ```

### CI/CD
DentiaPro includes a GitHub Actions workflow for automated testing and deployment.

---

## Contribution Guidelines

We welcome contributions to DentiaPro! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to your branch (`git push origin feature/your-feature-name`).
5. Create a Pull Request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

## Contact

For questions or support, contact the DentiaPro team:
Mohamed ESSRHIR
- **GitHub:** Outtacosmos-ai
- **Email:** m.essrhir98@gmail.com
- **Phone:** (+212)6 288-37712

Yahya OUBEDDA
- **GitHub:** Velvetvi123
- **Email:** yahya.oub@gmail.com
- **Phone:** (+212)6 19159531 