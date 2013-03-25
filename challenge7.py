#!/usr/bin/python

# challenge7.py
# Rackspace API Challenge #7 -- Creating servers and adding to LB
# Blatantly stolen from open source documentation

import os
import pyrax
import time

# Defines

network_wait = 30		# Number of seconds to wait between attempts


creds_file = os.path.expanduser("~/.rax_api")
pyrax.set_credential_file(creds_file)


cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers

img_id = [img for img in cs.images.list()
    if "CentOS 6" in img.name][0]
flavor_id = [flavor for flavor in cs.flavors.list()
    if flavor.ram == 512][0]


server1 = cs.servers.create("server1", img_id, flavor_id)
s1_id = server1.id
server2 = cs.servers.create("server2", img_id, flavor_id)
s2_id = server2.id

# The servers won't have their networks assigned immediately, so
# wait until they do.
while not (server1.networks and server2.networks):
    time.sleep(network_wait)
    server1 = cs.servers.get(s1_id)
    server2 = cs.servers.get(s2_id)

# Get the private network IPs for the servers
server1_ip = server1.networks["private"][0]
server2_ip = server2.networks["private"][0]

# Use the IPs to create the nodes
node1 = clb.Node(address=server1_ip, port=80, condition="ENABLED")
node2 = clb.Node(address=server2_ip, port=80, condition="ENABLED")

# Create the Virtual IP
vip = clb.VirtualIP(type="PUBLIC")

lb = clb.create("example_lb", port=80, protocol="HTTP",
        nodes=[node1, node2], virtual_ips=[vip])

