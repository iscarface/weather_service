# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY ../requirements.txt /app/requirements.txt

# Update pip
RUN python -m pip install -U pip


# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000
