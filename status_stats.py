#!/usr/bin/env python

# Will generate status statistics

from __future__ import print_function
import argparse
import hashlib
import json
from sqlalchemy import create_engine, distinct
from sqlalchemy.orm import sessionmaker
from data_models import Base, Job
import plotly.plotly as py
import plotly.graph_objs as go

parser = argparse.ArgumentParser()
parser.add_argument("config", help="The JSON config file to load.")
parser.add_argument("-v", "--verbose", help="Run verbosely",
        action="store_true")
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

def log(line):
    if args.verbose:
        print(line)
# First, obtain all the possible statuses from the db
statuses = [a[0] for a in session.query(distinct(Job.status)).all()]

for repo in config['repos']:
    if not repo.has_key('path'):
        print("A repo entry is missing needed keys!")
        print(repo)
        sys.exit(1)

    log("> Processing '{0}'".format(repo['path']))

    if repo.has_key('hash'):
        hash_id = repo['hash']
    else:
        hash_id = hashlib.md5(repo['path']).hexdigest()

    num_builds = session.query(Job).filter(Job.repo_hash == hash_id).count()

    for s in statuses:
        fname = "{0}.{1}.status_log".format(hash_id, s)
        with open(fname, 'w') as f:
            log(">> Processing status '{0}'".format(s))
            results = session.query(Job).filter(
                Job.repo_hash == hash_id).filter(Job.status == s).all()
            print("Total builds: {0}".format(num_builds), file=f)
            print("Total buils with '{0}': {1}".format(s, len(results)),
                    file=f)
            print("-"*40, file=f)
            data = {}
            for r in results:
                timestamp = r.start_time.strftime("%Y-%m-%d")
                if timestamp in data:
                    data[timestamp] += 1
                else:
                    data[timestamp] = 1

            keys = sorted(data)
            x = []
            y = []
            count = 1
            for k in keys:
                print("{0}:{1}".format(count, "*" * data[k]), file=f)
                x.append(count)
                y.append(data[k])
                count += 1

            plot_data = [go.Scatter(x=x, y=y)]
            py.plot(plot_data, filename="{0}.html".format(fname),
                    sharing="secret", auto_open=False)
