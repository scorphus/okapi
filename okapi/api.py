"""
okapi.api
~~~~~~~~~
This module implements the Requests API while storing valuable information into mongodb.  
"""

import mongo
import pymongo
import requests
import time
import urlparse 

from pymongo import MongoClient 

# TODO:
# Depends on how we want to calculate the time to
# receieve the request form Home Depots API.
# There are several choices. 
# Time.time, Time.clock, and a class from request called elapsed
# I have a test file that makes it seem that time.clock is fastest but is it most accurate?!?
# I have used time.clock for now

class Api:
	
	def __init__(self, project_name, host, port):
		""" initialization of class api"""
		self.host = host
		self.port = port
		self.project_name = project_name

		client = MongoClient(self.host, self.port)	
		self.db = client.okapi

	def request(self, method, url, **kwargs):
		"""calls a method of request library while storing info about api call into mongo db"""
		start = time.clock()
		res = requests.request(method, url, **kwargs)
		end = time.clock()

		content = ''

		if not res.ok:
			content = res.content

		host = urlparse.urlparse(res.url)

		data = {'time': (end - start),
			   	'project_name': self.project_name,
			   	'status_code': res.status_code,
			   	'url': res.url,
			   	'host': host.hostname,
			   	'method': method,
			   	'content': content
		}

		datas = self.db.datas
		data_id = datas.insert(data)

		return res

	def get(self, url, **kwargs):
		return self.request('GET', url, **kwargs)

	def delete(self, url, **kwargs):
		return self.request('DELETE', url, **kwargs)

	def post(self, url, **kwargs):
		return self.request('POST', url, **kwargs)

	def put(self, url, **kwargs):
		return self.request('PUT', url, **kwargs)
