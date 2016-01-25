#!/usr/bin/env python

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Boolean

Base = declarative_base()

class Job(Base):
    """Completed CircleCI jobs"""

    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    repo_hash = Column(String, index=True)
    build_number = Column(Integer)
    branch = Column(String, index=True)
    status = Column(String, index=True)
    outcome = Column(String, index=True)
    build_time = Column(Integer)
    start_time = Column(Date, index=True)

    def __repr__(self):
        return "<Job(build_number='{0}', branch='{1}', status='{2}', outcome='{3}')>".format(
                self.build_number, self.branch, self.status, self.outcome)

class Error(Base):
    """Error statistics"""

    __tablename__ = "errors"
    id = Column(Integer, primary_key=True)
    step = Column(String, index=True)
    count = Column(Integer)

    def __repr__(self):
        return "<Error(step='{0}', count='{1}')>".format(self.step,
                self.count)
