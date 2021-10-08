#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#title           :developer_create.py
#description     :Create Mazinger Database (MongoDB - Developers)
#author		     :MRP/mrp - Mauro Rosero P.
#date            :20210401
#version         :0.6    
#usage		     :db_create.py [-h] [-H HOST] [-P PORT] [-u USER] -p PASSWORD -c USERID USERNAME EMAIL TIMEZONE
#notes           :
#==============================================================================

import pymongo
import datetime, pytz
import argparse
import sys

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
		eprint("Error on MongoDB Mazinger Database: %s" % db_name)
		res = None
	return res

def create_developers(db, user_name, user_id, user_email, user_timezone):
	try:
		created = False
		col = db['devops_users']
		today = datetime.datetime.now(tz=None)
		if col.find_one() == None:
			record = { 
						"userid": user_id, 
						"username": user_name,
						"user_email": [user_email],
						"user_tz": user_timezone,
						"developer": True,
						"manager": True,
						"date_created": today, 
						"date_updated": today
						}
			r_id = col.insert_one(record)
		else:
			r_filter = { "userid": user_id }
			r_values = { "$set": { "date_updated": today,
									"username": user_name,
									"developer": True,
									"user_email": [user_email],
									"user_tz": user_timezone,
						} }
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
	requiredName.add_argument('-c', '--cols',
						required=True,
						dest='cols',
						metavar=('USERID', 'NAME', 'EMAIL', 'TIMEZONE'),
						help='Provide developer info',
						type=str,
						nargs=4
						)
	args = parser.parse_args()
	db_host = find_prefix(args.host)
	dbc = connect_mongodb(db_host[0], db_host[1], args.user, args.password)
	if dbc == None:
		return 1
	dbase = db_setting(dbc, u"mazingerdb")
	print(dbase)
	if dbase == None:
		return 2
	if not create_developers(dbase, args.cols[1], args.cols[0], args.cols[2], args.cols[3]):
		return 3
	return 0

if __name__ == '__main__':
	sys.exit(main())
