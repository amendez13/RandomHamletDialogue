Setup Development Container
* docker pull ubuntu:24.04
* docker images // list all available images and verify ubuntu:24.04 is present
* Ensure a Dockerfile is present in the current directory.
* docker build -t dev-container:24.04 .
* docker run -it --name dev-cont-instance dev-container:24.04
* docker container rm -f dev-cont-instance // This command forcibly removes the container

Python setup:

* sudo apt install python3.12-venv
* python3 -m venv path/to/venv.
* ./path/to/venv./bin/pip install --upgrade requests urllib3 bs4
* ./path/to/venv./bin/python3 main.py 
