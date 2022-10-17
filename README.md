
# InSPRIRES Platform Web Application

This repository contains the source files and build and deployment instructions for the InSPIRES Open Platform project, under the bigger european InSPIRES Project [(Ingenious Science shops to promote Participatory Innovation, Research and Equity in Science)](https://cordis.europa.eu/project/rcn/210055/factsheet/en).

## Architecture Overview

![Architecture Overview](https://cloud.carrotpiracy.com/index.php/s/scRc3Gw6NCjdXrx/preview)

The repository provides the neccesary elements to spawn a docker process and configure an Apache VirtualHost to serve from one single server two domains, each acting respectively as front-end and back-end. If it were necesary in the future, the front end and back end can be separated into two different servers.

The host's apache acts as an **SSL termination**, and all intra-host communication is performed safe from outside interference and with unencrypted HTTP sockets.

All configuration parameters can be adapted using the provided `.env.sample file`.

# Deployment Instructions

## Step by Step

To deploy the platform to a new server, first make sure you have installed all of the required software in the section `Required software on Host`.

1. Clone the repository to a folder. It is suggested to use `/opt/docker/<folder>` for this purpose.
1. Copy the `.env.sample` file at the root of the folder to `.env`. Ignore other `.env.sample` files inside the `django` and `vuetify` folders.
1. Configure the new `.env` file to your needs.
1. Create a new Apache2 VirtualHost using the `apache.vhost.conf` file in the root folder. Configure this host with proper SSL certificates and adapt to your needs. Make sure the domains and ports in the virtualhost configuration match with the `.env` file you previously configured.
1. Restart Apache2 if you haven't done so yet.
1. Open port `80` and `443` on the server's firewall.
1. At the root folder. run the command `docker-compose up`
1. All docker containers should spin up and open their configured ports internally to the machine.
1. The setup is complete.

### Required software on Host

1. Docker-CE
2. Apache2 (mod_headers + mod_ssl)

HTTPS Certificates can be obtained throuh letsencrypt `certbot-auto` software.

## Custom HTTPS header for Django

As HTTPS is handled by Apache on the host system, communication between the host
and docker is donde through unencrypted HTTP sockets. Due to this, Django needs a way
to know that it is behind an HTTPS proxy to generate reverse URLS with the `https://`
protocol. As included in the provided virtualhost files, this header is passed by apache
to the UWGSI server executing the WSGI django application.

The HTTP Header used is `X-Forwarded-Proto`, which later is transformed into
`HTTP_X_FORWARDED_PROTO` by the system and correctly interpreted by the `server/settings.py`
configuration.


## Development Instructions

### For frontend development

**Requirements**
- NodeJS 10 LTS

**Setup steps**
1. Open `vuetify` folder in VSCode.
1. Copy `.env.sample` to `.env`
1. Edit values in `.env` file to point to a remote server
    that is running the backend.
1. Run `npm run serve` to start the local testing environment in order
    to start development of the frontend. HMR is setup so there is no
    need to refresh the browser on code changes.

### For backend development:

You can configure the backend to use an SQLite DB and no Redis so that a simple dev enviroment can be bootstrapped easily.

**Requirements**
- Python3 + PIP

**Setup steps**
1. Open `vuetify` folder in VSCode.
1. Copy `.env.sample` to `.env`
1. Edit values in `.env` to suit your needs.
1. Run `virtualenv env` to create a new Python Virtual environment.
1. Activate the virtual environment (this depends on wether you run windows or linux, please check instructions specific to your OS)
1. Install the necesary packages `pip install -r requirements`.
1. Create the DB tables: `python manage.py migrate`
1. Run the server through the console: `python manage.py runserver localhost:<port defined in frontend .env>`
