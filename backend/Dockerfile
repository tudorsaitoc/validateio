FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl gcc && rm -rf /var/lib/apt/lists/*

# Install core Python dependencies first
RUN pip install --no-cache-dir \
    fastapi==0.109.0 \
    uvicorn[standard]==0.25.0 \
    pydantic==2.5.3 \
    pydantic-settings==2.1.0 \
    python-dotenv==1.0.0 \
    httpx==0.25.2

# Copy all files
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8080

# Create a startup script that uses hybrid main
RUN echo '#!/usr/bin/env python3\nimport os\nos.environ["PORT"] = os.environ.get("PORT", "8080")\nimport main_hybrid' > start_hybrid.py

# Run the hybrid app
CMD ["python", "main_hybrid.py"]