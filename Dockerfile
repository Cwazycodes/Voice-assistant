# Use a Python base image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libasound2-dev \
    libav-tools \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Specify the command to run the application
CMD ["python", "app.py"]  # Replace with your actual entry point if different
