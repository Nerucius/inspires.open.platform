# LMS Web Application Project

Repository for the LMS project.

## Deployment Instructions

### Software on Host

1. Docker-CE
2. Apache2 (mod_headers + mod_ssl)

HTTPS Certificates can be obtained throuh letsencrypt `certbot-auto` software.

### Custom HTTPS header for Django

As HTTPS is handled by Apache on the host system, communication between the host
and docker is donde through unencrypted HTTP sockets. Due to this, Django needs a way
to know that it is behind an HTTPS proxy to generate reverse URLS with the `https://`
protocol. As included in the provided virtualhost files, this header is passed by apache
to the UWGSI server executing the WSGI django application.

The HTTP Header used is `X-Forwarded-Proto`, which later is transformed into
`HTTP_X_FORWARDED_PROTO` by the system and correctly interpreted by the `server/settings.py`
configuration.

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
