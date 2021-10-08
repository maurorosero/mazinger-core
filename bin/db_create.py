#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#title           :db_create.py
#description     :Create Mazinger Database (MongoDB)
#author		     :MRP/mrp - Mauro Rosero P.
#date            :20210401
#version         :0.6    
#usage		     :db_create.py [-h] [-H HOST] [-P PORT] [-u USER] -p PASSWORD -c CODE NAME TIMEZONE
#notes           :CODE = COMPANY CODE, NAME = COMPANY NAME, TIMEZONE = PLATFORM TIMEZONE
#=====================================================================================================

import pymongo
import datetime, pytz
import argparse
import os, sys
import csv

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def find_prefix(host):
	pattern = u'://'
	h_prefix = u"mongodb+srv" + pattern
	if host.find(pattern) == -1:
		h_host = h_prefix + host
	else:
		h_host = host
	h_host = host.split(pattern)
	h_host[0] = h_host[0] + pattern
	return h_host
		
def connect_mongodb(db_prefix, db_server, db_user, db_pass):
	connection = db_prefix + db_user + ":" + db_pass + "@" + db_server + "/test?retryWrites=true"
	try:
		db_client = pymongo.MongoClient(connection)
	except pymongo.errors.InvalidURI:
		eprint("Invalid MongoDB Connection Uri: %s" % connection)
		db_client = None
	except pymongo.errors.PyMongoError:
		eprint("Error on MongoDB Connection")
		db_client = None	
	return db_client

def db_setting(dbc, db_name):
	try:
		res = dbc[db_name]
	except pymongo.errors.PyMongoError:
		res = None
	return res

def create_company(db, company_name, company_code, company_timezone):
	try:
		created = False
		col = db['companies']
		today = datetime.datetime.now(tz=None)
		if col.find_one() == None:
			record = { 
						"code_id": company_code, 
						"name": company_name,
						"date_timezone": company_timezone, 
						"date_created": today, 
						"date_updated": today
						}
			r_id = col.insert_one(record)
		else:
			r_filter = { "code_id": company_code }
			r_values = { "$set": { "date_updated": today, "date_timezone": company_timezone } }
			r_id = col.update_one(r_filter, r_values)
		created = True
	except pymongo.errors.PyMongoError:
		print('error')
		created = False
	return created
	
def main():
	parser = argparse.ArgumentParser(add_help=True)
	parser.add_argument('-H', '--host',
						default='mongodb://localhost',
						dest='host',
						help='Provide destination host. Defaults to localhost',
						type=str
						)
	parser.add_argument('-P', '--port',
						default='27017',
						dest='port',
						help='Provide destination port. Defaults to 27017',
						type=str
						)
	parser.add_argument('-u', '--user',
						default='admin',
						dest='user',
						help='Provide login user. Defaults to admin',
						type=str
						)
	requiredName = parser.add_argument_group('required arguments')
	requiredName.add_argument('-p', '--pass',
						required=True,
						dest='password',
						help='Provide login password',
						type=str
						)
	requiredName.add_argument('-c', '--company',
						required=True,
						dest='company',
						metavar=('CODE', 'NAME', 'TIMEZONE'),
						help='Provide company info',
						type=str,
						nargs=3
						)
	args = parser.parse_args()
	db_host = find_prefix(args.host)
	dbc = connect_mongodb(db_host[0], db_host[1], args.user, args.password)
	if dbc == None:
		return 1
	dbase = db_setting(dbc, u"mazingerdb")
	if dbase == None:
		return 2
	if not create_company(dbase, args.company[1], args.company[0], args.company[2]):
		return 3
	return 0

if __name__ == '__main__':
	sys.exit(main())
