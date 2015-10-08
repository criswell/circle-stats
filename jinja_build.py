#!/usr/bin/env python

# Based upon original code by Sam Hart
# https://bitbucket.org/criswell/sam_resume

from __future__ import print_function
import sys
import datetime
import os
import json
import hashlib
try:
    from jinja2 import Template
    from jinja2 import FileSystemLoader
    from jinja2.environment import Environment
except ImportError:
    print("Uh-oh! Looks like you don't have jinja2 installed!")
    print("Go to http://jinja.pocoo.org/ and install it please!")
    sys.exit(1)

def usage():
    print("jinga_build.py config.json file.html output_dir/ <templateDirectories>")
    print("\nBuilds a file specified by 'file.html', dumping to STDOUT the resulting HTML.\n")
    print("<templateDirectories> is one or more directories for templates to be housed,")
    print("separated by commas.\n")
    print("'config.json' is the JSON configuration file.")
    print("'output_dir/' is where the resulting generated HTML files will go.")

if len(sys.argv) < 2 or len(sys.argv) > 5:
    usage()
    sys.exit()

filename = sys.argv[2]
templateFile = open(filename, 'r')
rawTemplate = templateFile.readlines()
templateFile.close()

strTemplate = "".join(rawTemplate)

output_dir = sys.argv[3]

env = Environment()
if len(sys.argv) == 5:
    p = sys.argv[4].split(',')
    env.loader = FileSystemLoader(p)
else:
    env.loader = FileSystemLoader(".")

config = {}
with open(sys.argv[1], 'r') as f:
    config = json.load(f)

if not config.has_key('repos'):
    print("Error parsing config file! Missing 'repos' stanza!")
    print(config)
    sys.exit(1)

for repo in config['repos']:
    page_title = repo.get('title', '').format(date=datetime.datetime.now())
    hash_id = hashlib.md5(repo['path']).hexdigest()

    template = env.from_string(strTemplate)
    rendered = template.render(page_title=page_title)

    print(rendered)
