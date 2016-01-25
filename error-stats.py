#!/usr/bin/env python

# This script does a deep dive into the data collected previously, and performs
# an analysis of the errors.

from __future__ import print_function
import sys
import subprocess
import json
import argparse
import hashlib
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_models import Base, Job, Error

parser = argparse.ArgumentParser()
parser.add_argument("config", help="The JSON config file to load.")
parser.add_argument("-v", "--verbose", help="Run verbosely",
        action="store_true")
args = parser.parse_args()

config = {}

with open(args.config, 'r') as f:
    config = json.load(f)

if not config.has_key('repos') or not config.has_key('database-url'):
    print("Error parsing config file!")
    print(config)
    sys.exit(1)

engine = create_engine(config['database-url'])
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
BASE_API_URL = 'https://circleci.com/api/v1'

def get_cmd_output(command):
    output = subprocess.Popen(command.split(),
            stdout=subprocess.PIPE).communicate()[0].decode('ascii')
    return output.strip()

def log(line):
    if args.verbose:
        print(line)

for repo in config['repos']:
    if not repo.has_key('path') or not repo.has_key('highlight-branches'):
        print("A repo entry is missing needed keys!")
        print(repo)
        sys.exit(1)

    log("> Processing '{0}'".format(repo['path']))

    hash_id = hashlib.md5(repo['path']).hexdigest()

    q = session.query(Job).filter(Job.repo_hash == hash_id)
    q = q.filter(Job.outcome == 'failed')
    results = q.all()
    circle_user = get_cmd_output('git -C {0} config git-circle.user'.format(
        repo['path']))
    circle_project = get_cmd_output(
            'git -C {0} config git-circle.project'.format(repo['path']))
    log(">--> user: {0}, project: {1}".format(circle_user, circle_project))

    for result in results:
        print(result.build_number)
