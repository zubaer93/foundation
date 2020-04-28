#!/usr/bin/env python3.6


from subprocess import call
import sys

PROJECT_DIR = sys.argv[1]

call(['bash', '-c', f"./run.py up && cd ../{PROJECT_DIR}&& ./run.py all up && cd ../backbone && ./run.py log styline-web"])



