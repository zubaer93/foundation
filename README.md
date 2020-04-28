# Docker Proxy Container with Letsencrypt

- Table of Contents
  - [Introduction](#introduction)
  - [Documentation](#documentation)
    - [Folder Structure](#folder-structure)
  - [Quick Start](#quick-start)

## Introduction
1. This starts [nginx](https://hub.docker.com/_/nginx/), [docker-gen](https://github.com/jwilder/docker-gen), [rsyslog](https://www.rsyslog.com), [logrotate](https://github.com/blacklabelops/logrotate) and [letsencrypt-nginx-proxy-companion](https://github.com/JrCs/docker-letsencrypt-nginx-proxy-companion) containers.
2. **letsencrypt-nginx-proxy-companion** is only used in non local environmens to generates valid SSL certificate from [letsencrypt](https://letsencrypt.org/).
3. for local environment self signed certificates can be created using `./volumes/certs/local/create-local-ca.sh` and `./volumes/certs/local/create-local-cert.sh` scripts.
3. **nginx** works as reverse proxy for other applications running in docker containers



## Documentation
### Folder Structure
```bash
├── dockerfiles                     # dockerfiles and related files for containers
│   ├── rsyslog
│   │  ├── Dockerfile
│   │  ├── rsyslog.conf
├── volumes                         # all folders inside this are mounted in docker container
│   ├── certs                       # ssl certificates in here
│   │  ├── letsencrypt              # letsencrypt generated ssl certificates
│   │     ├── .gitignore
│   │  ├──local                     # locally generated using create-local-cert.sh
│   │     ├── create-local-ca.sh    # creates a local root CA SSL cerficiates
│   │     ├── create-local-cert.sh  # creates self signed cerficates for development
│   │     ├── .gitignore            # only track bash scripts in here
│   ├── conf.d
│   │   ├── .gitgignore
│   │   ├── custom.conf             # nginx configuration override
│   ├── html
│   │   ├── .gitgignore
│   ├── log                         # all container log files are stored here
│   ├── rsyslog.d                   # dokcer-gen generated config files for rsyslog
│   ├── templates
│   │   ├── docker-gen.cfg          # docker-gen configuration template
│   │   ├── ngnx.tmpl               # downloaded from https://raw.githubusercontent.com/jwilder/docker-gen/master/templates/nginx.tmpl
│   │   ├── logrotate.tmpl          # template for generating logrotate configuration files
│   │   ├── rsyslog.tmpl            # template for generating rsyslog configuration files
│   ├── vhost.d                     # virtualhost specific nginx config can be put here i.e. www.example.com
│   │   ├── .gitgignore
├── docker-compose.override.yml     # development config
├── docker-compose.production.yml   # production config
├── docker-compose.yml              # common config
├── initialize.py                   # run certificate scripts to create root CA and ssl certificates
├── README.md
├── run.py                          # to start, stop, log proxy containers
```

## Quick Start

#### Install these and start docker service
1. Docker. Instructions: [Windows](https://docs.docker.com/docker-for-windows/install/#start-docker-for-windows),
  [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/#os-requirements),
  [Mac](https://docs.docker.com/docker-for-mac/install/#install-and-run-docker-for-mac)
2. Docker Compose. [Instructions](https://docs.docker.com/compose/install/#install-compose)
3. Install python 3.6

#### Initialize
1. Create `.env` file and put `COMPOSE_PROJECT_NAME=foundation`. this is used by docker compose files.
```bash
echo "COMPOSE_PROJECT_NAME=foundation" > .env
```
2. Create `.env.run` file and put `development`. for non local environemnt this should be `production`
```bash
echo "development" > .env.run
```
3. Create self signed certificates of your application for local development
```bash
# create root CA. only once
cd ./volumes/certs/local
./create-local-ca.sh
# create self signed certificates
./create-local-cert.sh local.www.example.com
# update /etc/hosts file with above domain names pointing to 127.0.0.1.
127.0.0.1  local.www.example.com
```

#### Start proxy containers. tasks('up', 'down', 'log')
```bash
# ./run.py [TASK] [CONTAINER]
./run.py log example-web

# check if containers are running
docker ps
# should show two containers named **nginx**, **docker-gen**, **rsyslog**, **logrotate** for 'local' environement
```

#### Nginx Customisation
1. There is one file `./volumes/conf.d/custom.conf` which applies to all domains served by nginx
2. for Domain specific customisation create a file in `./voloumes/vhost.d/` directory. name of the file should match the domain name. put your customisation there and restart nginx
```bash
echo "client_max_body_size 20M;" > ./volumes/vhost.d/local.www.example.com
```
