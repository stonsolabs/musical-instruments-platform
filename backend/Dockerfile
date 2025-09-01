# Use the official Azure Functions Python base image
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

# Set environment variables
ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true \
    PYTHONPATH=/home/site/wwwroot

# Copy requirements and install dependencies
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# Copy function app
COPY . /home/site/wwwroot

# Set the working directory
WORKDIR /home/site/wwwroot

# Ensure proper permissions
RUN chmod -R 755 /home/site/wwwroot