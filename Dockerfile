# WidowMind Core Dockerfile t

FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Expose internal Flask port
EXPOSE 5000

# Run the Flask app using Gunicorn
CMD ["gunicorn", "arachnocore_launcher:app", "--bind", "0.0.0.0:5000", "--workers", "4"]
