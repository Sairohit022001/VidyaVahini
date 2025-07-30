FROM python:3.11-slim

WORKDIR /app

# Update pip and setuptools first
RUN pip install --upgrade pip setuptools wheel

# Copy only requirements first for caching
COPY requirements.txt .

# Install NumPy first to avoid version conflicts
RUN pip install --no-cache-dir "numpy>=1.24.0,<2.0.0"

# Install ONNX Runtime with specific version
RUN pip install --no-cache-dir "onnxruntime==1.15.0"

# Install the rest of the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variable for Google credentials JSON inside container
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/vidyavahini-tts-e8ebc3dc20f2.json"

# Document the port exposed by the container (optional but recommended)
EXPOSE 8080

# Command to start the FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
