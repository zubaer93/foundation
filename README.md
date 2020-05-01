# Docker Proxy Container with Letsencrypt

- Table of Contents
  - [Introduction](#introduction)
  - [Quick Start](#quick-start)

## Introduction
1. This starts [nginx](https://hub.docker.com/_/nginx/), [docker-gen](https://github.com/jwilder/docker-gen), [rsyslog](https://www.rsyslog.com), [logrotate](https://github.com/blacklabelops/logrotate) and [letsencrypt-nginx-proxy-companion](https://github.com/JrCs/docker-letsencrypt-nginx-proxy-companion) containers.
2. **letsencrypt-nginx-proxy-companion** is only used in non local environmens to generates valid SSL certificate from [letsencrypt](https://letsencrypt.org/).
3. for local environment self signed certificates can be created using `./volumes/certs/local/create-local-ca.sh` and `./volumes/certs/local/create-local-cert.sh` scripts.
3. **nginx** works as reverse proxy for other applications running in docker containers

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

#### Start proxy containers. tasks('up', 'down', 'log')

1. For up, down, build and log your containers use the following pattern
```bash
# ./run.py [TASK] [CONTAINER]
Example :
./run.py up
./run.py down
./run.py log example-web

# check if containers are running
docker ps
# should show four containers named **nginx**, **docker-gen**, **rsyslog**, **logrotate** for 'local' environement
```

#### Serve your docker application with nginx

1. Expose 80 or any other port from your container
2. Set a 'VIRTUAL_HOST=local.your-site-name.com' in your docker environment variable
3. For staging or production deployment put 'LETSENCRYPT_HOST=your-site-name.com' and 'LETSENCRYPT_EMAIL=your-email@email.com' in docker environment variable
3. Make sure your application and foundation is is the same network (check the foundation yml file)
4. Now Build your application
5. For local development you can create self signed certificate
```
# create root CA. only once
cd ./volumes/certs/local
./create-local-ca.sh
# create self signed certificates
./create-local-cert.sh local.www.example.com
# update /etc/hosts file with above domain names pointing to 127.0.0.1.
127.0.0.1  local.www.example.com
```

#### Nginx Customization
1. There is one file `./volumes/conf.d/custom.conf` which applies to all domains served by nginx
2. for Domain specific customisation create a file in `./voloumes/vhost.d/` directory. name of the file should match the domain name. put your customisation there and restart nginx
```bash
echo "client_max_body_size 20M;" > ./volumes/vhost.d/local.www.example.com
```
