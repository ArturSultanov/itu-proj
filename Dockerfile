FROM python:3.12.7-slim
LABEL name="ITU API Backend"

# Set working directory inside the container
WORKDIR /app

# Copy only the required files and directories
COPY requirements.txt .
COPY backend backend

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the FastAPI port
EXPOSE 8000

# Set environment variables
ENV DATABASE_URL=sqlite+aiosqlite:///./backend/database/game.db
ENV PYTHONPATH=/app

# Command to start the FastAPI application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
