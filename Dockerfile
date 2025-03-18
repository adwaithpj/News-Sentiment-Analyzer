# Use official Python image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy only required files first (to leverage Docker caching)
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry install --no-root

# Copy the remaining project files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Default command to run the application
CMD ["poetry", "run", "python", "api.py"]
