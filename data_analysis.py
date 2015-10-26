#!/usr/bin/env python

# Data analysis module, not intended to be run from the command line

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_models import Base, Job

MILLI_TO_MINUTES = 0.000016667

class Data:
    def __init__(self, hash_id, branch):
        self.hash_id = hash_id
        self.branch = branch
        self.data = {}
        self.data_type = None
        self.duration = None

def dateback_from_business_days(from_date, back_days, holidays=[]):
    """Determine the number of days to go back if we exclude weekends.

        Given the desired number of days to go back, 'back_days', the date to
        start from, 'from_date', and an optional list of holidays, compute and
        return the *actual* days to go back and an array of excluded days, if
        we exclude weekends and holidays.

        Params:
            'from_date' : The date to start from.
            'back_days' : The total, non-weekend, non-holiday, days to go back
            'holidays'  : Optional array containing datetime days of holidays

        Returns:
            ( total_days_back, excluded_days ) where
            'total_days_back' : The actual days to go back
            'excluded_days'   : An array of excluded days in DataAnalysis
                                expected format.
    """
    business_days_to_add = back_days
    current_date = from_date
    total_days_back = 0
    excluded_days = []
    while business_days_to_add > 0:
        current_date += datetime.timedelta(days=-1)
        weekday = current_date.weekday()
        if weekday >= 5: # sunday = 6
            excluded_days.append(current_date)
            continue
        elif current_date in holidays:
            excluded_days.append(current_date.strftime("%Y-%m-%d"))
            continue
        else:
            total_days_back += 1
        business_days_to_add -= 1
    return (total_days_back, excluded_days)

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

        Returns:
            data : A Data object. data.data is an unsorted dictionary of
                   'day'=>'average', where average is in minutes.
        """
        running_joke = self._session.query(Job).filter(Job.repo_hash == hash_id)
        today = datetime.date.today().strftime("%Y-%m-%d")
        (actual_days_back, excluded_days) = dateback_from_business_days(
                datetime.date.today(), num_days)
        days_delta = datetime.timedelta(days=actual_days_back)
        start_day = (datetime.date.today() - days_delta).strftime("%Y-%m-%d")
        running_joke = running_joke.filter(Job.start_time.between(
            start_day, today))
        running_joke = running_joke.filter(Job.outcome.in_(outcomes))
        if branch is not None:
            running_joke = running_joke.filter(Job.branch == branch)

        results = running_joke.all()
        data = Data(hash_id, branch)
        data.data_type = "average"
        data.duration = num_days
        avg_total = 0
        num_iter = 0
        daily_avg_total = {}
        daily_num_iter = {}
        for result in results:
            if result.start_time in excluded_days:
                continue
            if not daily_avg_total.has_key(result.start_time):
                daily_avg_total[result.start_time] = 0
            if not daily_num_iter.has_key(result.start_time):
                daily_num_iter[result.start_time] = 0

            daily_num_iter[result.start_time] = \
                    daily_num_iter[result.start_time] + 1
            daily_avg_total[result.start_time] = \
                    daily_avg_total[result.start_time] + result.build_time
            avg_total = avg_total + result.build_time
            num_iter = num_iter + 1

        for key in daily_avg_total.keys():
            data.data[key] = \
                (daily_avg_total[key] / daily_num_iter[key]) * MILLI_TO_MINUTES

        #data.average = (avg_total / num_iter) * MILLI_TO_MINUTES
        return data

    def pad_missing_days(self, datasets):
        """Given a list of datasets, pad out missing days. Return list of
        datasets with all days present"""
        days = []
        for dataset in datasets:
            for key in dataset.data.keys():
                if key not in days:
                    days.append(key)

        new_datasets = []

        for s in datasets:
            missing = list(set(days) - set(s.data.keys()))
            for m in missing:
                s.data[m] = 0
            new_datasets.append(s)

        return new_datasets
