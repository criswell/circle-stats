#!/usr/bin/env python

# Data analysis module, not intended to be run from the command line

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_models import Base, Job

class DataAnalysis:
    def __init__(self, db_url):
        """Initialize DataAnalysis object.

        'db_url' is the URL for the database according the SQLAlchemy format.
        """
        self._engine = create_engine(db_url)
        S = sessionmaker()
        S.configure(bind=self._engine)
        self._session = S()

    def compute_averages(self, hash_id, num_days, outcomes, branch=None,
            exclude_weekends=True):
        """Compute the averages for the past 'num_days' days.

        Parameters:
            hash_id : the hash id for the repo
            num_days : the number of days to go back
            outcomes : a tuple of the outcomes we're interested in
            branch : the branch to restrict to (if None, will use all branches)
            exclude_weekends : if True, will exclude weekends from results
        """
        running_joke = self._session.query(Job).filter(Job.repo_hash == hash_id)
        today = datetime.date.today().strftime("%Y-%m-%d")
        days_delta = datetime.timedelta(days=num_days)
        start_day = (datetime.date.today() - days_delta).strftime("%Y-%m-%d")
        running_joke = running_joke.filter(Job.start_time.between(
            start_day, today))
        running_joke = running_joke.filter(Job.outcome.in_(outcomes))
        if branch is not None:
            running_joke = running_joke.filter(Job.branch == branch)

        results = running_joke.all()
        for result in results:
            print result

