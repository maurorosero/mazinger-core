#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#title           :db_tasks.py
#description     :Create Mazinger Inventory Tasks Definitions (MongoDB)
#author		     :MRP/mrp - Mauro Rosero P.
#date            :20210401
#version         :0.6    
#usage		     :db_groups.py [-h] [-H HOST] [-P PORT] [-u USER] -p PASSWORD -f taskfile 
#notes           :
#=====================================================================================================

import pymongo
import datetime, pytz
import argparse
import os, sys
import json

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def read_taskfile(task_file):
	tasks = {}
	try:
		if os.path.exists(task_file):
			with open(task_file) as json_file:
				tasks = json.load(json_file)
	except ValueError as err:
		tasks = False
	return tasks
	
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
	
def company_exists(db, company_code):
	cia = db['companies']
	ok = False
	result = cia.find({"code_id": company_code}, { "_id": 0 }) 
	if result.count() > 0: 
		ok = True
	return ok
	
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
	
def update_tasks(db, tasks):
	try:
		created = False
		today = datetime.datetime.now(tz=None)
		tsk = db['requests']
		t_segments = tasks['request_type'].split(u".")
		if tsk.find_one() == None:
			if t-segments[2] == 'N':
				tasks['request_id'] = '000001'
			tasks["date_created"] = today
			tasks["date_updated"] = today
			r_id = tsk.insert_one(tasks)
		elif tasks['request_id'] == u"" or tasks['request_id'] == u"0" and t-segments[2] == 'N':
			tasks["date_created"] = today
			tasks["date_updated"] = today
			r_id = tsk.insert_one(tasks)
		else:
			t_filter = { u'teamvar': record['teamvar'] }
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
	requiredName.add_argument('-t', '--task',
						required=True,
						dest='taskfile',
						help='Provide task definition file path',
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
	task_dict = read_taskfile(args.taskfile)
	if task_dict == {}:
		return 4
	if not task_dict:
		return 5
	if not company_exists(dbase, tasks_dict[u'customer_key']):
			if u'new_company' in tasks_dict:
				if not create_company(dbase, tasks_dict[u'customer_key'][u'name'], tasks_dict[u'customer_key'], tasks_dict[u'customer_key'][u'date_timezone']):
					return 6
			else:
				return 6
	if not update_tasks(dbase, task_dict):
		return 3
	return 0

if __name__ == '__main__':
	sys.exit(main())
