FROM ubuntu:24.04
RUN apt update && apt upgrade -y && apt-get clean
RUN apt install -y curl vim python3 sudo && \
	apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m -s /bin/bash userdev
RUN usermod -aG sudo userdev
RUN echo "userdev ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/userdev
USER userdev
CMD ["/bin/bash"]
