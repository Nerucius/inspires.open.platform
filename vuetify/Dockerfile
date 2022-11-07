# FROM node:10-alpine
# FROM node:alpine
# Needed for Prerender SPA Framework
FROM alekzonder/puppeteer:latest
# FROM node:12-alpine

USER root

# Install python/pip and build tools (vuetify build requirement)
# ENV PYTHONUNBUFFERED=1
# RUN apk add --update --no-cache python3 make g++ && ln -sf python3 /usr/bin/python
# RUN python3 -m ensurepip
# RUN pip3 install --no-cache --upgrade pip setuptools

RUN mkdir /vuetify
WORKDIR /vuetify

# Install depencies
COPY package*.json ./
RUN npm install

# Copy project and build
COPY . .

WORKDIR /vuetify
RUN chmod a+x docker-entrypoint.sh
ENTRYPOINT [ "sh", "-c", "./docker-entrypoint.sh" ]
