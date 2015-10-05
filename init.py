#!/usr/bin/env python

# This script initializes a project for the CircleCI stats scripts

from __future__ import print_function
import sys
import os
import os.path
import json
import argparse
from data_models import Base

parser = argparse.ArgumentParser()
parser.add_argument("config", help="The JSON config file to load.")
args = parser.parse_args()

config = {}

with open(args.config, 'r') as f:
    config = json.load(f)

if not config.has_key('database-url'):
    print("Error! No 'database-url' setting in config!")
    print(config)
    sys.exit(1)

from sqlalchemy import create_engine
engine = create_engine(config['database-url'])

from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

