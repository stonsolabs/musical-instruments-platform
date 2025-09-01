# Use the official Azure Functions Python base image
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

# Set environment variables
ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

# Set the working directory
WORKDIR /home/site/wwwroot

# Copy requirements and install dependencies first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app
COPY . .

# Ensure the function app file is executable
RUN chmod +x function_app.py

# Verify the structure
RUN ls -la /home/site/wwwroot/ && ls -la /home/site/wwwroot/app/