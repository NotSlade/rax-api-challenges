#!/usr/bin/python

# challenge5.py
# Rackspace API Challenge #5 -- Create new CDB 

import os
import pyrax
import time

# Defines

wait_time = 30			# Time to wait between refreshes
instance_name = 'test_instance'
database_name = 'test'
user_name = 'test'
user_pass = 'test'

creds_file = os.path.expanduser("~/.rax_api")
pyrax.set_credential_file(creds_file)


cdb = pyrax.cloud_databases
ram_type = [flavor for flavor in cdb.list_flavors()
	                if flavor.ram == 512][0]
db_instance = cdb.create(instance_name, flavor=ram_type, volume=1)

while True:
    try:
	db = db_instance.create_database(database_name)
    except:
	print 'Sleeping for db'
	time.sleep(wait_time)
	continue
    break


while True:
    try:
	user = db_instance.create_user(user_name, user_pass, database_names=[db])
    except:
	print 'Sleeping for user.'
	time.sleep(wait_time)
	continue
    break

print
print "User '%s' has been created on instance '%s'." % (user_name, instance_name)
print
