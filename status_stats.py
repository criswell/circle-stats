#!/usr/bin/env python

# Will generate status statistics

from __future__ import print_function
import argparse
import hashlib
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_models import Base, Job

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

def log(line):
    if args.verbose:
        print(line)

for repo in config['repos']:
    if not repo.has_key('path'):
        print("A repo entry is missing needed keys!")
        print(repo)
        sys.exit(1)

    log("> Processing '{0}'".format(repo['path']))

    if repo.has_key('hash'):
        hash_id = repo['hash']
    else:
        hash_id = hashlib.md5(repo['path']).hexdigest()

    # First, obtain all the possible statuses from the db
    q = session.query(Job).filter(Job.repo_hash == hash_id)
    q = q.distinct(Job.status)
    results = q.all()

    print(results)
