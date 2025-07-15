# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Expose port (Cloud Run will bind here)
EXPOSE 8080

# Command to run the app
CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "8080"]
