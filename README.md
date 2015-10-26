# Usage

Setup a config json file.

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

...

Profit

