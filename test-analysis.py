#!/usr/bin/env python

from __future__ import print_function
from data_analysis import DataAnalysis
import json
import hashlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("config", help="The JSON config file to load.")
args = parser.parse_args()

config = {}

with open(args.config, 'r') as f:
    config = json.load(f)

weekday_only = config.get('weekdays-only', False)
# fail hard if not found
db_url = config['database-url']

da = DataAnalysis(db_url)

num_days = config['max_days']
outcomes = ['success']
weekdays_only = config['weekdays-only']

for repo in config['repos']:
    hash_id = hashlib.md5(repo['path']).hexdigest()
    outcomes =

    da.compute_averages(hash_id, num_days, outcomes, None, weekdays_only)

