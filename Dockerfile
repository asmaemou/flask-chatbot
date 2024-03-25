# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at the working directory
COPY . .

# Make sure the `api` directory is available in the Docker image
COPY api ./api


# Copy the entire index directory into the container at /usr/src/app/index
COPY index /usr/src/app/index


# Run index.py when the container launches
CMD ["python", "api/index.py"]