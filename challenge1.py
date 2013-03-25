#!/usr/bin/python

# challenge1.py
# Rackspace API Challenge #1 -- Spin up three new servers

import os
import pyrax
import time

# Defines

num_servers = 3			# Total number of servers to make
wait_time = 30			# Time to wait between refreshes
prefix = 'TestServer'		# Prefix for server names


creds_file = os.path.expanduser("~/.rax_api")
pyrax.set_credential_file(creds_file)

cs = pyrax.cloudservers
ids = []
passwords = []
networks = []
names = []

for i in range(1, num_servers + 1):
	
	server_name = prefix + str(i)
	image_type = [img for img in cs.images.list()
		if "CentOS 6" in img.name][0]
	ram_type = [flavor for flavor in cs.flavors.list()
		if flavor.ram == 512][0]
	
	server = cs.servers.create(server_name, image_type.id, ram_type.id)

	names.append(server.name)
	ids.append(server.id)
	passwords.append(server.adminPass)



for curr_id in ids:

    server = cs.servers.get(curr_id)
    while str(server.networks) == '{}':
        time.sleep(wait_time)
        server = cs.servers.get(curr_id)

    networks.append(server.networks)


while len(networks):
    print "********"
    name = names.pop(0)
    print "Server name: " + str(name)
    network = networks.pop(0)
    print "Networks: " + str(network)
    password = passwords.pop(0)
    print "Root password: " + str(password) + "\n"
