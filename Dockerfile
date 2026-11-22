# Dockerfile
# ─────────────────────────────────────────────────────────────────
# Packages the Flask API into a Docker container image.
# Trivy scans this built image for CVEs in the OS and Python libs.
#
# How Docker works (simple version):
#   FROM  → start from an existing base image (Python pre-installed)
#   COPY  → copy files from your machine into the container
#   RUN   → run a command inside the container while building
#   CMD   → command that runs when the container starts
# ─────────────────────────────────────────────────────────────────

# Base image: official Python 3.12 (slim = smaller, fewer packages = fewer CVEs)
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependencies file first (Docker caches this layer — faster rebuilds)
COPY app/requirements.txt .

# Install Python dependencies (--no-cache-dir keeps the image smaller)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY app/ .

# Tell Docker this container listens on port 5000
EXPOSE 5000

# Command to run when the container starts
CMD ["python", "main.py"]
