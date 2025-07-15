# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port 8080
EXPOSE 8080

# Run the FastAPI app on the required port
CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "8080"]
