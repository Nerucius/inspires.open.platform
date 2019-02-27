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

# Setup env variables for debug
# ENV VUE_APP_API_SERVER=http://localhost:8080
# ENV NODE_ENV=development

CMD [ "npm", "run", "build:docker" ]
