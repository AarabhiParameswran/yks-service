# Base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install New Relic agent
RUN pip install newrelic

# Copy the application code
COPY . .

# Copy New Relic config file
COPY newrelic.ini .

# Set environment variable to tell New Relic where the config is
ENV NEW_RELIC_CONFIG_FILE=/app/newrelic.ini

# Expose the application port
EXPOSE 8001

# Run the FastAPI application via New Relic agent
CMD ["newrelic-admin", "run-program", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--proxy-headers", "--forwarded-allow-ips", "*"]
