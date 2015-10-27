# The Missing CircleCI Statistics Dashboard

This collection of scripts generate a CircleCI statistics dashboard for one
or more projects.

The generated files are HTML and can be viewed in a browser. The default
templates display each chart full-window, and cycle from one chart to the next.
If you'd like something else, create your own template files.

You can see a sample output here https://output.jsbin.com/qemolutewe

## Installation

The scripts require the following things:

* Python 2.7+
* Jinja2
* SQLAlchemy
* git-circle

These can be installed using the `requirements.txt` file with Pip:

```
# For system-wide install
pip install -r requirements.txt

# For local-user install
pip install --user -r requirements.txt
```

Additionally, the current template files require [ChartJS](http://chartjs.org/),
but they load it dynamically when the page loads.

Once these are installed, then simply execute the scripts in this repository.

# Usage

Setup a config json file. See [sample-config.js](sample-config.js) for an
example of the configuration file.

Init the database:

```
./init.py config.json
```

Run the data-collection (probably from cron daily):

```
./data-collecy.py config.json
```

Run the HTML builder script (probably from cron daily):

```
./jinja_build.py config.json html/index.html output html
```

View the resulting HTML file(s) in a browser.

Once in a while (maybe monthly), run the cull script to clean up old entries:

```
./cull-data.py -v config.json
```

...

Profit

