#!/usr/bin/env python3.6


from subprocess import call
from pathlib import Path
import sys



TASK = sys.argv[1]
ENVIRONMENT = Path('.env.run').read_text().rstrip()

CONTAINER = sys.argv[2] if len(sys.argv) > 2 else 'nginx'
COMPOSE_FILES = ' -f docker-compose.yml -f docker-compose.production.yml ' if ENVIRONMENT == 'production' \
    else ' -f docker-compose.yml -f docker-compose.override.yml '

print('ENVIRONMENT: ' + ENVIRONMENT)
print('COMPOSE FILES: ' + COMPOSE_FILES)

def up():
    call(['bash', '-c', 'docker network create --subnet=172.28.0.0/16 own-network'])
    call(['bash', '-c', 'docker-compose ' + COMPOSE_FILES + ' up -d '])

def down():
    call(['bash', '-c', 'docker-compose ' + COMPOSE_FILES + ' down'])
    call(['bash', '-c', 'docker network rm own-network'])

def build():
    call(['bash', '-c', 'docker-compose ' + COMPOSE_FILES + ' build '])

def log():
    call(['bash', '-c', f"sudo tail -f ./volumes/log/{CONTAINER}/container.log"])

def bash():
    call(['bash', '-c', f"docker-compose {COMPOSE_FILES} exec {CONTAINER} bash"])

if TASK == 'up':
    up()
elif TASK == 'down':
    down()
elif TASK == 'log':
    log()
elif TASK == 'bash':
    bash()
elif TASK == 'dup':
    down()
    up()
elif TASK == 'bup':
    down()
    build()
    up()
else:
    call(['bash', '-c', 'echo "No such command found)"'])






