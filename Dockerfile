# Use the official Python image as a parent image
FROM python:3.9-slim

# Set environment variables for FastAPI
ENV APP_HOME /app
WORKDIR $APP_HOME

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8000
EXPOSE 8001
RUN pip install uvicorn
RUN pip install python-multipart

# Command to run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
