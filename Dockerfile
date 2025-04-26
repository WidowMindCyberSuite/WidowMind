# WidowMind Core Dockerfile

FROM python:3.11-slim

# Set working directory inside container
WORKDIR /WidowMind/app

# Copy app source code into container
COPY app/ /WidowMind/app/

# Install Python dependencies
RUN pip install --no-cache-dir -r /WidowMind/app/widowmindcore/requirements.txt

# Expose internal Flask port
EXPOSE 5000

# Launch the app using Gunicorn (high performance server)
CMD ["gunicorn", "widowmindcore:app", "--bind", "0.0.0.0:5000", "--workers", "4"]

