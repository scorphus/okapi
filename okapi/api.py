# Copyright 2014 Red Beacon, Inc.  All Rights Reserved
#
# This code, and all derivative work, is the exclusive property of
# Red Beacon, Inc. and may not be used without Red Beacon, Inc.'s
# authorization.
#
# Author: Gobind Ball

"""
okapi.api
~~~~~~~~~
This module implements the Requests API while storing valuable information into mongodb.
"""

import datetime
import logging
import requests
import time
import urlparse

from pymongo import errors
from pymongo import MongoClient

logger = logging.getLogger(__name__)


class Api(object):
    TIMEOUT = 5000

    def __init__(self, project_name, mongodb_uri='mongodb://localhost', connect_timeout_ms=TIMEOUT):
        """Initialization of class api.

        See http://docs.mongodb.org/manual/reference/connection-string/ for
        more information about the mongodb_uri parameter.
        """
        self.project_name = project_name

        try:
            client = MongoClient(mongodb_uri, connectTimeoutMS=connect_timeout_ms)
            self.db = client.okapi
        except (errors.ConnectionFailure, errors.InvalidURI):
            self.db = None
            logger.error('Unable to connect to MongoDB at %s', mongodb_uri)

    def _save_request(self, method, url, status_code, content, start):
        if self.db is not None:

            date = datetime.datetime.utcnow()
            host = urlparse.urlparse(url)
            hour = format(date.time().hour, '02')
            minute = format(date.time().minute, '02')

            time_bucket = [
                "{} {}:{}-minute".format(date.date(), hour, minute),
                "{} {}-hour".format(date.date(), hour),
                "{}-day".format(date.date()),
            ]

            data = {
                'content': content,
                'date': date,
                'host': host.hostname,
                'method': method,
                'response_time': time.time() - start,
                'status_code': status_code,
                'url': url,
                'time_bucket': time_bucket,
            }

            try:
                # As Google Docs optimization #3 (Lose resolution)
                collection = self.db["{}_raw".format(self.project_name)]
                # the w parameter is making the insertion to db asynchronous
                collection.insert(data, w=0)
            except:
                logger.exception('Error writing to MongoDB')

    def request(self, method, url, **kwargs):
        """calls a method of request library while storing info about api call into mongo db"""
        content = ''
        status_code = None
        start = time.time()
        try:
            res = requests.request(method, url, **kwargs)
            status_code = res.status_code
            if not res.ok:
                content = res.content
            self._save_request(method, url, status_code, content, start)
        except requests.exceptions.ConnectionError:
            content = 'Connection error'
            self._save_request(method, url, status_code, content, start)
            raise
        except requests.exceptions.HTTPError:
            content = 'HTTP error'
            self._save_request(method, url, status_code, content, start)
            raise
        except requests.exceptions.Timeout:
            content = 'Timeout'
            self._save_request(method, url, status_code, content, start)
            raise

        return res

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request('DELETE', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('POST', url, **kwargs)

    def put(self, url, **kwargs):
        return self.request('PUT', url, **kwargs)