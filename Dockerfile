FROM jenkins/jenkins:lts-alpine

# Install Docker
USER root
RUN apk update && \
    apk add --no-cache docker
USER jenkins
