# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install system dependencies including PostgreSQL development headers and libraries
RUN apt-get update && \
    apt-get install -y libpq-dev gcc postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js and npm
RUN apt-get update && apt-get install -y nodejs npm

# Change directory to the scripts folder and install dependencies
WORKDIR /app/scripts
RUN npm install
RUN chmod +x copydatabase.sh

# Change back to the root directory
WORKDIR /app

# Install dependencies for the main application
RUN npm install

# Install Unicorn
RUN pip install gunicorn

RUN apt-get install -y nano

# Expose the port that Unicorn will listen on
EXPOSE 4000


# Set execute permissions on the starting script
RUN chmod +x starting.sh

# Run the starting bash script
CMD ["./starting.sh"]
