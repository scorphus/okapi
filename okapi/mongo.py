"""
okapi.mongo
~~~~~~~~~
Creates a mongo client (as of right now)
"""

# necessary libraries and modules for this script
import requests
import pymongo

from pymongo import MongoClient 

client = MongoClient()

def create_client(host, port):
	client = MongoClient(host,port)	
	return client