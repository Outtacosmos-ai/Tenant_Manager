# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for PostgreSQL (libpq) and any needed OS packages
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements file (if you keep it in backend/requirements.txt, adjust path)
COPY backend/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Expose port 8000 (if you need to bypass Nginx during dev)
EXPOSE 8000

# Default command (Gunicorn) - overridden by docker-compose command if you like
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
