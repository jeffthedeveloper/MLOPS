# Stage 1: Build a base with dependencies
# Using a specific version is better for reproducibility
FROM python:3.8-slim-buster AS base

# Set the working directory
WORKDIR /app

# Create a non-root user for security
RUN useradd --create-home appuser
USER appuser

# Copy only the requirements file first to leverage Docker layer caching
COPY --chown=appuser:appuser requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Create the final, lean image
FROM python:3.8-slim-buster

WORKDIR /app

# Copy the non-root user from the base stage
COPY --from=base /etc/passwd /etc/passwd
COPY --from=base /etc/group /etc/group
COPY --from=base /home/appuser /home/appuser

# Copy the installed dependencies from the base stage
COPY --from=base /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

# Copy the application code
COPY --chown=appuser:appuser . .

# Set the user
USER appuser

# Expose the port the app runs on
EXPOSE 5000

# Run the application using a production-ready WSGI server like Gunicorn
# Add 'gunicorn' to your requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
