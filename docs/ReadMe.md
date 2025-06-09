Set up Container
* docker pull python:3.12-slim
* docker images // list all available images and verify python:3.12-slim is present
* Ensure a Dockerfile is present in the current directory.
* docker build -t hamlet-diag-container:3.12-slim .
* docker run -it --name hamlet-diag-container-instance hamlet-diag-container:3.12-slim
* docker container rm -f hamlet-diag-container-instance // This command forcibly removes the container
* docker container rm -f hamlet-diag-container-instance ; docker build -t hamlet-diag-container:3.12-slim .; docker run -it --name hamlet-diag-container-instance hamlet-diag-container:3.12-slim

Python setup:

* sudo apt install python3.12-venv
* python3 -m venv path/to/venv.
* ./path/to/venv./bin/pip install --upgrade requests urllib3 bs4
* ./path/to/venv./bin/python3 main.py 
