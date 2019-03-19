# FROM node:10-alpine
# Needed for Prerender SPA Framework
FROM alekzonder/puppeteer:latest

USER root

RUN mkdir /vuetify
WORKDIR /vuetify

# Install depencies
COPY package*.json ./
RUN npm install

# Copy project and build
COPY . .

ENTRYPOINT [ "sh", "-c", "docker-entrypoint.sh" ]
