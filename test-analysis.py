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

num_days = config['max-days']
outcomes = ['success']
weekdays_only = config['weekdays-only']

def display(data):
    pre = data.branch
    if pre is None:
        pre = ''

    days = sorted(data.data.keys())
    for i in days:
         print("{0}>{1}:{2}".format(pre, i,data.data[i]))
    print("{0}-----{1}".format(pre, data.average))
    print("{0}-----{1}".format(pre, len(data.data)))

for repo in config['repos']:
    hash_id = hashlib.md5(repo['path']).hexdigest()

    d = []
    d.append(da.compute_averages(hash_id, num_days, outcomes, None,
        weekdays_only))
    for branch in repo['highlight-branches']:
        d.append(da.compute_averages(hash_id, num_days, outcomes,
            branch, weekdays_only))
    d = da.pad_missing_days(d)
    for i in d:
        display(i)

    print("max_days: {0}\tweekdays_only: {1}".format(num_days, weekdays_only))
