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
HEADERS = {'Accept' : 'application/json'}

def get_cmd_output(command):
    output = subprocess.Popen(command.split(),
            stdout=subprocess.PIPE).communicate()[0].decode('ascii')
    return output.strip()

def log(line):
    if args.verbose:
        print(line)

def increment_point(step, hash_id):
    running_joke = session.query(Error).filter(Error.repo_hash == hash_id)
    running_joke = running_joke.filter(Error.step == step)
    if running_joke.count() < 1:
        e = Error(repo_hash=hash_id, step=step, count=1)
        session.add(e)
    else:
        e = running_joke.first()
        e.count = e.count + 1
        session.add(e)
    session.commit()


def process_steps(steps, hash_id):
    for step in steps:
        step_name = step['name']
        for action in step['actions']:
            if action['failed']:
                increment_point(step_name, hash_id)

for repo in config['repos']:
    if not repo.has_key('path') or not repo.has_key('highlight-branches'):
        print("A repo entry is missing needed keys!")
        print(repo)
        sys.exit(1)

    log("> Processing '{0}'".format(repo['path']))

    if repo.has_key('hash'):
        hash_id = repo['hash']
    else:
        hash_id = hashlib.md5(repo['path']).hexdigest()

    # First, drop the table
    delme = session.query(Error).delete()

    q = session.query(Job).filter(Job.repo_hash == hash_id)
    q = q.filter(Job.outcome == 'failed')
    results = q.all()
    circle_user = get_cmd_output('git -C {0} config git-circle.user'.format(
        repo['path']))
    circle_project = get_cmd_output(
            'git -C {0} config git-circle.project'.format(repo['path']))
    circle_token = get_cmd_output('git -C {0} config git-circle.token'.format(
        repo['path']))
    log(">--> user: {0}, project: {1}".format(circle_user, circle_project))
    log("=================")

    i = 0

    for result in results:
        i = i + 1
        log("\tBuild: {0}\t\t{1}/{2}".format(result.build_number, i,
            len(results)))
        api_url = "{0}/project/{1}/{2}/{3}?circle-token={4}".format(
            BASE_API_URL, circle_user, circle_project, result.build_number,
            circle_token)
        r = requests.get(api_url, headers=HEADERS)
        if r.status_code != 200:
            log("\t>>> ERROR RETRIEVING THAT BUILD!")
        else:
            data = r.json()
            process_steps(data['steps'], hash_id)
