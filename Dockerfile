# WidowMind Core Dockerfile

# 1. Use a minimal, secure base image
FROM python:3.11-slim AS base

# 2. Set working directory inside the container
WORKDIR /app

# 3. Pre-install pip upgrades for security + performance
RUN pip install --upgrade pip setuptools wheel

# 4. Copy only requirements first (for better Docker caching)
COPY app/requirements.txt /app/requirements.txt

# 5. Install Python dependencies separately
RUN pip install --no-cache-dir -r /app/requirements.txt

# 6. Now copy the full application code
COPY app/widowmindcore /app/widowmindcore

# 7. Expose the application port
EXPOSE 5000

# 8. Run the server with Gunicorn (production WSGI server)
CMD ["gunicorn", "widowmindcore:app", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "--timeout", "120"]
