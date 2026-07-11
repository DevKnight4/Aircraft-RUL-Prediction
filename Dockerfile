FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (LightGBM requires libgomp1)
RUN apt-get update && apt-get install -y libgomp1 && rm -rf /var/lib/apt/lists/*

# Install python dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy necessary directories for the backend to function
COPY backend/ backend/
COPY models/ models/
COPY src/ src/
COPY data/raw/ data/raw/

# Expose the API port
EXPOSE 8000

# Start the FastAPI server using the dynamically assigned PORT (or fallback to 8000)
CMD uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}
