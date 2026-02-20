# version
FROM python:3.11-slim
# folder to add code and modules for container
WORKDIR /app
# linux commmands on startup
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*
# python modules
RUN pip install --no-cache-dir psutil rich prometheus_client flask
# copy code to docker container
COPY . .
# install package for entrypoint
RUN pip install -e .
ENTRYPOINT ["sentinel"]
