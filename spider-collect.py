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
#import sys
#import subprocess
#import datetime
#import csv
#import json
import argparse
#import hashlib
#from dateutil.parser import parse
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
#from data_models import Base, Job

parser = argparse.ArgumentParser()
parser.add_argument("config", help="The JSON config file to load.")
parser.add_argument("-v", "--verbose", help="Run verbosely",
        action="store_true")
args = parser.parse_args()


