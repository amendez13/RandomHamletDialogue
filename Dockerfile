FROM python:3.12-slim

# Update and upgrade packages, then clean up
RUN apt update && apt upgrade -y && apt install -y vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user and grant sudo privileges
RUN useradd -m -s /bin/bash userdev

# Switch to userdev
USER userdev
WORKDIR /home/userdev

# Set up virtual environment
RUN python3 -m venv venv

# Copy requirements.txt and install dependencies
COPY --chown=userdev:userdev requirements.txt .
RUN venv/bin/pip install --upgrade pip==23.2.1 && \
    venv/bin/pip install -r requirements.txt

# Copy your main.py into the container
# Ensure that main.py is located in the same directory as the Dockerfile or adjust the path accordingly.
COPY --chown=userdev:userdev main.py .

# Set the command to run the Python script in the virtual environment
ENTRYPOINT ["venv/bin/python3", "main.py"]