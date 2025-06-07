FROM ubuntu:24.04

# Update and upgrade packages, then clean up
RUN apt update
RUN apt upgrade -y && apt-get clean

RUN apt install -y curl vim python3 python3-venv python3-pip sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user and grant sudo privileges
RUN useradd -m -s /bin/bash userdev && \
    usermod -aG sudo userdev && \
    echo "userdev ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/userdev

# Switch to userdev
USER userdev
WORKDIR /home/userdev

# Create and set up virtual environment
RUN python3 -m venv /home/userdev/venv && \
    /home/userdev/venv/bin/pip install --upgrade pip && \
    /home/userdev/venv/bin/pip install --upgrade requests urllib3 beautifulsoup4

# Copy your main.py into the container
# Ensure that main.py is located in the same directory as the Dockerfile or adjust the path accordingly.
COPY main.py /home/userdev/main.py

# Set the command to run the Python script in the virtual environment
CMD ["/home/userdev/venv/bin/python3", "/home/userdev/main.py"]