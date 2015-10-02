#!/usr/bin/env python

# This script initializes a project for the CircleCI stats scripts

from __future__ import print_function
import sys
import os.path
import json
import argparse
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument("config", help="The JSON config file to load.")
parser.add_argument("-f", "--force", help="Force re-init", action="store_true")
args = parser.parse_args()

config = {}

with open(args.config, 'r') as f:
    config = json.load(f)

if not config.has_key('data-file'):
    print("Error! No 'data-file' setting in config!")
    print(config)
    sys.exit(1)

if os.path.isfile(config['data-file']):
    if args.force:
        print("DB file found, forcing re-init!")


conn = sqlite3.connect(config['data-file'])

# Create the DB schema
