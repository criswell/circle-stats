#!/usr/bin/env python

# Culls old records from the db

from __future__ import print_function
import datetime
import json
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import argparse
from data_models import Job

parser = argparse.ArgumentParser()
parser.add_argument("config", help="The JSON config file to load.")
parser.add_argument("-v", "--verbose", help="Run verbosely",
        action="store_true")
args = parser.parse_args()

config = {}

with open(args.config, 'r') as f:
    config = json.load(f)

engine = create_engine(config['database-url'])
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

def log(line):
    if args.verbose:
        print(line)

for repo in config['repos']:
    if not 'path' in repo:
        print("A repo entry is missing needed keys!")
        print(repo)
        sys.exit(1)

    hash_id = hashlib.md5(repo['path']).hexdigest()
    running_joke = session.query(Job).filter(Job.repo_hash == hash_id)
    days_delta = datetime.timedelta(days=config['max-days'])
    start_day = (datetime.date.today() - days_delta).strftime("%Y-%m-%d")
    running_joke = running_joke.filter(Job.start_time < start_day)

    results = running_joke.all()
    for result in results:
        log("Deleting : {0}".format(result))
        session.delete(result)

    log("Deleted {0} entries".format(len(results)))

    session.commit()

