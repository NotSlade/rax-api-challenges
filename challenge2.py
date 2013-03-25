#!/usr/bin/python

# challenge2.py
# Rackspace API Challenge #2 -- Copying a server

import os
import pyrax
import time

# Defines

postfix = 'New'			# String to append onto server name
image_wait = 30			# Number of seconds to wait between attempts
max_attempts = 40		# Number of times to attempt to build
attempts = 0



creds_file = os.path.expanduser("~/.rax_api")
pyrax.set_credential_file(creds_file)

cs = pyrax.cloudservers
servers = cs.servers.list()

srv_dict = {}
print "Select a server to copy."
for pos, srv in enumerate(servers):
	print "%s: %s" % (pos, srv.name)
	srv_dict[str(pos)] = srv.id
selection = None
while selection not in srv_dict:
	if selection is not None:
		print " -- Invalid choice"
	selection = raw_input("Enter the number for your choice: ")

server_id = srv_dict[selection]
img_id = cs.servers.create_image(server_id, pyrax.utils.random_name(12))

ram_type = [flavor for flavor in cs.flavors.list()
	if flavor.ram == 512][0]

server = cs.servers.get(server_id)
server_name = server.name


# Try to create the server from the image.  Assume the image is still being
# processed and try again if it fails.

while True:

    if(attempts == max_attempts):
	print("ERROR: The server has failed to build after " + attempts + "attempts.")
	print("Terminating script")
	sys.exit()

    try:
	server = cs.servers.create(server_name + postfix, img_id, ram_type.id)
    except:
	time.sleep(image_wait)
	attempts += 1
	continue
    break


# Output
print "Name:", server.name
print "ID:", server.id
print "Admin Password:", server.adminPass

# Desired cleanup here
