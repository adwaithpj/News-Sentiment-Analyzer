# Use official Python image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy project files to the container
COPY . .

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry install --no-root

# Expose FastAPI and Streamlit ports
EXPOSE 8000
