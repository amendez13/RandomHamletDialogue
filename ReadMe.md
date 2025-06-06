Setup Development Container
* docker pull ubuntu:24.04
* docker images // list all available images and verify ubuntu:24.04 is present
* Ensure a Dockerfile is present in the current directory.
* docker build -t dev-container:24.04 .
* docker run -it --name dev-cont-instance dev-container:24.04
* docker container rm -f dev-cont-instance // This command forcibly removes the container
