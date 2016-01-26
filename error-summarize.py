#!/usr/bin/env python

# This script summarizes the error stats from the error table

from __future__ import print_function
import sys
import json
import argparse
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from data_models import Base, Job, Error

parser = argparse.ArgumentParser()
parser.add_argument("config", help="The JSON config file to load.")
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

for repo in config['repos']:
    if not repo.has_key('path') or not repo.has_key('highlight-branches'):
        print("A repo entry is missing needed keys!")
        print(repo)
        sys.exit(1)

    if repo.has_key('hash'):
        hash_id = repo['hash']
    else:
        hash_id = hashlib.md5(repo['path']).hexdigest()
    header = "REPO : {0}, HASH: {1}".format(repo['path'], hash_id)
    print("-" * len(header))
    print(header)
    print("-" * len(header))
    q = session.query(Error).filter(Error.repo_hash == hash_id)
    q = q.order_by(desc(Error.count))
    results = q.all()

    print("   NUM_ERRORS\tSTEP")
    for result in results:
        print("   {0}\t\t{1}".format(result.count, result.step))

    print()
