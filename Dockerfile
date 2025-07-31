# ---------- Base Image ----------
FROM python:3.12-slim

# Install UV (lightweight package manager)
RUN pip install --no-cache-dir uv

# Set work directory
WORKDIR /app

# Copy project files
COPY pyproject.toml ./
COPY main.py models.py database.py ./

# Install dependencies using UV (from pyproject.toml)
RUN uv sync --frozen

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI app
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
