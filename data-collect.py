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
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument("config", help="The JSON config file to load.")
args = parser.parse_args()

config = {}

with open(args.config, 'r') as f:
    config = json.load(f)

if not config.has_key('repos') or not config.has_key('data-file'):
    print("Error parsing data file!")
    print(config)
    sys.exit(1)

date_offset = datetime.timedelta()

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

date_limit = str(datetime.date.today() + date_offset)

conn = sqlite3.connect(config['data-file'])

def process_row(row):
    pass

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

