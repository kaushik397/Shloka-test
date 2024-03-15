# Use the official Python image as the base image
FROM python:3.10-slim

# Set environment variables
ENV APP_HOME /app
ENV PORT 8000

# Create the application directory
WORKDIR $APP_HOME

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port on which the FastAPI application will run
EXPOSE $PORT

# Command to run the FastAPI application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
