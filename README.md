# LMS Web Application Project

Repository for the LMS project.

## Build Instructions

### Frontend Development Only

**Requirements**
- NodeJS 10 LTS

**Setup steps**
1. Open `vuetify` folder in VSCode.
1. Copy `vuetify\.env.sample` to `vuetify\.env`
1. Edit values in `.env` file to point to a remote server
    that is running the backend.
1. local testing DNS needs to be on the same domain as the server
    in the previous step.
1. run `npm run serve` to start the local testing environment in order
    to start development of the frontend. HMR is setup so there is no
    need to refresh the browser on code changes.

### Fullstack Development:

**Requirements**
- Linux OS
- Docker
- Docker Compose

**Setup steps**
1. Open main repository folder in VSCode
1. Copy `.env.sample` to `.env`
1. Adjust .env file variables to your setup
1. run docker-compose up --build
1. Code will run in containers and is accessible on ports defined
    in .env file. Please note that the containers are set up to autorefresh on code changes in the host.
