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
import requests
import time
import urlparse

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# TODO:
# Depends on how we want to calculate the time to
# receieve the request form Home Depots API.
# There are several choices.
# Time.time, Time.clock, and a class from request called elapsed
# I have a test file that makes it seem that time.clock is fastest but is it most accurate?!?
# I have used time.clock for now

class Api(object):

    def __init__(self, project_name, host, port):
        """ initialization of class api"""
        self.host = host
        self.port = port
        self.project_name = project_name

        try:
            client = MongoClient(self.host, self.port)
            self.db = client.okapi
        except ConnectionFailure:
            self.db = None

    def request(self, method, url, **kwargs):
        """calls a method of request library while storing info about api call into mongo db"""
        start = time.clock()
        res = requests.request(method, url, **kwargs)
        end = time.clock()

        if self.db is not None:

            content = ''

            if not res.ok:
                content = res.content

                date = datetime.datetime.utcnow()
                host = urlparse.urlparse(res.url)

                data = {'content': content,
                        'date': date,
                        'host': host.hostname,
                        'method': method,
                        'project_name': self.project_name,
                        'response_time': (end - start),
                        'status_code': res.status_code,
                        'url': res.url,
                    }

                datas = self.db.datas
                datas.insert(data)

        return res

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request('DELETE', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('POST', url, **kwargs)

    def put(self, url, **kwargs):
        return self.request('PUT', url, **kwargs)
