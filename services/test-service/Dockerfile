FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
COPY ../../requirements.txt ./base-requirements.txt
RUN pip install -r base-requirements.txt && \
    pip install -r requirements.txt

# Copy service code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]