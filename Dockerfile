# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app
COPY api/index .
# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at the working directory
COPY . .

# No need to copy the index folder separately as it is inside the api folder,
# which will be copied with the `COPY . .` command above

# Run index.py when the container launches
CMD ["python", "api/index.py"]

