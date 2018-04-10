FROM jenkins/jenkins:lts-alpine

# Install Docker and Docker Compose
USER root
RUN apk update && \
    apk add --no-cache docker python3 && \
    pip3 install --no-cache-dir docker-compose
USER jenkins
