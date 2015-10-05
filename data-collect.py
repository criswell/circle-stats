#!/usr/bin/env python

# This script collects data from git-circle and stores it in a format used by
# the other scripts in this repo

from __future__ import print_function
import sys
#import os
import subprocess
import datetime
import csv
import json
import argparse
import hashlib
from dateutil.parser import parse
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
    print("Error parsing data file!")
    print(config)
    sys.exit(1)

date_offset = datetime.timedelta()
zero_offset = datetime.timedelta()

if config.has_key('date-offset'):
    do = config['date-offset']
    days = do.get('days', 0)
    seconds = do.get('seconds', 0)
    microseconds = do.get('microseconds', 0)
    milliseconds = do.get('milliseconds', 0)
    minutes = do.get('minutes', 0)
    hours = do.get('hours', 0)
    weeks = do.get('weeks', 0)
    date_offset = datetime.timedelta(days=days, seconds=seconds,
            microseconds=microseconds, milliseconds=milliseconds,
            minutes=minutes, hours=hours, weeks=weeks)

if date_offset == zero_offset:
    query_date = datetime.date.today()
else:
    if config.get('weekdays-only', False):
        query_date = datetime.date.today() + date_offset
        while query_date.weekday() == 5 or query_date.weekday() == 6:
            query_date = query_date + date_offset

date_limit = str(query_date)

engine = create_engine(config['database-url'])
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

def log(line):
    if args.verbose:
        print(line)

def process_build(row):
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
                outcome=outcome, build_time=build_time, start_time=start_time)
        session.add(j)
    session.commit()

def process_row(row):
    if row[0] == 'BUILD':
        process_build(row)

for repo in config['repos']:
    if not repo.has_key('path') or not repo.has_key('highlight-branches'):
        print("A repo entry is missing needed keys!")
        print(repo)
        sys.exit(1)

    hash_id = hashlib.md5(repo['path']).hexdigest()
    # First, we get all branches
    git_cmd = "git -C {0} circle list-builds -ar -m --date={1}".format(
            repo['path'], date_limit)
    output = subprocess.Popen(git_cmd.split(),
            stdout=subprocess.PIPE).communicate()[0].decode('ascii')
    for row in csv.reader(output.splitlines(), delimiter=','):
        process_row(row)

