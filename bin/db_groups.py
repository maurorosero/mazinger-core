#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#title           :db_groups.py
#description     :Create Groups on Mazinger Database (MongoDB)
#author		     :MRP/mrp - Mauro Rosero P.
#date            :20210401
#version         :0.6    
#usage		     :db_groups.py [-h] [-H HOST] [-P PORT] [-u USER] -p PASSWORD -g groupfile -i invpath 
#notes           :
#=====================================================================================================

import pymongo
import datetime, pytz
import argparse
import os, sys
import csv

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def read_groups(groupfile):
	d_groups = []
	if os.path.exists(groupfile):
		with open(groupfile) as csvfile:
			csv_list = csv.DictReader(csvfile)
			d_groups = list(csv_list)
	return d_groups
	
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

def update_groups(db, groups):
	try:
		created = False
		today = datetime.datetime.now(tz=None)
		grp = db['groups']
		if grp.find_one() == None:
			for record in groups:
				record['plataform'] = False
				record['active'] = False
				if record['plataform'] != '0':
					record['plataform'] = True
				if record['active'] != '0':
					record['active'] = True
				r_id = grp.insert_one(record)
		else:
			glist = []
			g_ids = grp.update_many({}, {"$set" : { "active": False }})
			for record in groups:
				record['plataform'] = False
				record['active'] = False
				if record['plataform'] != '0':
					record['plataform'] = True
				if record['active'] != '0':
					record['active'] = True
				g_filter = { u'teamvar': record['teamvar'] }
			g_values = { "$set": record }
			g_id = grp.update_one(g_filter, g_values)
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
	requiredName.add_argument('-g', '--groupfile',
						required=True,
						dest='groupfile',
						help='Provide group definition file path',
						type=str
						)
	args = parser.parse_args()
	db_host = find_prefix(args.host)
	dbc = connect_mongodb(db_host[0], db_host[1], args.user, args.password)
	if dbc == None:
		return 1
	dbase = db_setting(dbc, u"mazingerdb")
	if dbase == None:
		return 2
	groups = read_groups(args.groupfile)
	if groups == []:
		return 4
	if not update_groups(dbase, groups):
		return 3
	return 0

if __name__ == '__main__':
	sys.exit(main())
