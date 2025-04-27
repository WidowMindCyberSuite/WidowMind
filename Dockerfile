# WidowMind Core - Best Practice Dockerfile

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y sqlite3 && \
    rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy WidowMind Core source code into container
COPY app/widowmindcore /app/widowmindcore

# Install Python dependencies directly from widowmindcore folder
RUN pip install --no-cache-dir -r /app/widowmindcore/requirements.txt

# Expose Flask server port
EXPOSE 5000

# Launch app using Gunicorn (high-performance production server)
CMD ["gunicorn", "widowmindcore:app", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "--timeout", "120"]

