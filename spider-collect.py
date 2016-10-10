#!/usr/bin/env python

# This script collects data in a slightly different way from data-collect. It
# starts with today (right now, in fact) and spiders its way back in time
# collecting build data as it goes. Build data is added to the database as
# usual.
#
# The main idea behind this script is to try and collect back-data when it's
# missing from the db, and do it in as least a disruptive way as possible. To
# accomplish this, it places random waits here and there between pulls.

from __future__ import print_function
import sys
import subprocess
import datetime
import time
import csv
import json
import argparse
import hashlib
import random
from dateutil.parser import parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_models import Base, Job

parser = argparse.ArgumentParser()
parser.add_argument("config", help="The JSON config file to load.")
parser.add_argument("-v", "--verbose", help="Run verbosely",
        action="store_true")
parser.add_argument("-d", help="The number of days back to go." + \
        " A '0' means to keep going backwards, forever. (Will have to " + \
        " kill the program for it to stop.)", type=int)
args = parser.parse_args()

config = {}

with open(args.config, 'r') as f:
    config = json.load(f)

if not config.has_key('repos') or not config.has_key('database-url'):
    print("Error parsing data file!")
    print(config)
    sys.exit(1)

engine = create_engine(config['database-url'])
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

def log(line):
    if args.verbose:
        print(line)

def process_build(hash_id, row):
    branch = row[1]
    build_number = row[2]
    status = row[4]
    outcome = row[5]
    build_time = row[11]
    start_time = parse(row[12]).date()
    if session.query(Job).filter(Job.build_number == build_number).count() < 1:
        log("{0}:{1}, {2}:{3}, {4} - {5}".format(branch, build_number, status,
            outcome, start_time, build_time))
        j = Job(build_number=build_number, branch=branch, status=status,
                outcome=outcome, build_time=build_time, start_time=start_time,
                repo_hash=hash_id)
        session.add(j)
    session.commit()

def process_row(hash_id, row):
    if row[0] == 'BUILD':
        process_build(hash_id, row)

for repo in config['repos']:
    if not repo.has_key('path') or not repo.has_key('highlight-branches'):
        print("A repo entry is missing needed keys!")
        print(repo)
        sys.exit(1)

    hash_id = hashlib.md5(repo['path']).hexdigest()
    count = 0
    while count <= args.d or args.d == 0:
        date_limit = str(datetime.date.today() - \
                datetime.timedelta(days=count))
        print(">>>>>> Day '{0}' : {1}".format(count, date_limit))
        git_cmd = "git -C {0} circle list-builds -ar -m --date={1}".format(
            repo['path'], date_limit)
        log(git_cmd)
        count = count + 1
        output = subprocess.Popen(git_cmd.split(),
                stdout=subprocess.PIPE).communicate()[0].decode('ascii')
        for row in csv.reader(output.splitlines(), delimiter=','):
            process_row(hash_id, row)
        time.sleep(random.randint(1,5))
