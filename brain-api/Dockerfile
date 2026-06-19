FROM python:3.9-slim
WORKDIR /app

# Copy requirements from either root or brain-api folder to handle any upload structure
COPY requirements.txt* ./
COPY brain-api/requirements.txt* ./

# Install dependencies based on which requirements.txt was found
RUN if [ -f requirements.txt ]; then \
        pip install --no-cache-dir -r requirements.txt; \
    elif [ -f brain-api/requirements.txt ]; then \
        pip install --no-cache-dir -r brain-api/requirements.txt; \
    fi

COPY . .

# Set PYTHONPATH to search both root and brain-api folder
ENV PYTHONPATH=/app:/app/brain-api

EXPOSE 8000

# Run uvicorn trying both paths to guarantee it starts
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} || uvicorn brain-api.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
