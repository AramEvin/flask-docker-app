# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory to /app inside the container
WORKDIR /app

# Copy only the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project (all files) into /app
COPY . .

# Set PYTHONPATH so Python can find your package at /app
ENV PYTHONPATH=/app

# Run the app
CMD ["python", "main.py"]
