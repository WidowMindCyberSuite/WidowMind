FROM python:3.11-slim

# Install required packages
RUN apt-get update && apt-get install -y \
    certbot \
    python3-certbot-nginx \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy app code
COPY ./app/widowmindcore ./widowmindcore
COPY ./app/database ./database
COPY ./app/logs ./logs
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask/Gunicorn port
EXPOSE 5000

# Entry point
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "widowmindcore.server:app"]"4", "-b", "0.0.0.0:5000", "widowmindcore.server:app"]