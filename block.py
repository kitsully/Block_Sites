#!/usr/local/bin/python

# Kristopher Sullivan 

import os
import csv
from os.path import expanduser
from plumbum import local
from plumbum import cli
from plumbum.cmd import ls, rm, touch, pwd, killall
home = expanduser("~")
flush_cache = "sudo killall -HUP mDNSResponder"
hosts_default = """##
# Host Database
#
# localhost is used to configure the loopback interface
# when the system is booting.  Do not change this entry.
##
127.0.0.1                  localhost
255.255.255.255	broadcasthost
::1                            localhost 
fe80::1%lo0	        localhost
"""

def un_block():
	local.cwd.chdir(home)
	local.cwd.chdir("../../private/etc/")
	touch("hosts")
	rm("hosts")
	touch("hosts")
	f = open("hosts", "r+")
	f.write(hosts_default)
	killall["-HUP", "mDNSResponder"]

def block_sites():
	print "works"
	local.cwd.chdir(home)
	local.cwd.chdir("Dropbox/Docs")
	blocked = []
	with open('blocked_sites.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in reader:
			for r in row:
				blocked.append(r)
	print blocked
	local.cwd.chdir(home)
	local.cwd.chdir("../../private/etc/")
	rm("hosts")
	touch("hosts")
	with open("hosts", "r+") as hosts:
		hosts.write(hosts_default)
		# hosts.write("\n")
		for item in blocked:
			site = "127.0.0.1 " + item + "\n"
			site = "127.0.0.1 " + "www." + item + "\n"
			hosts.write(site)
	killall["-HUP", "mDNSResponder"]

class MyApp(cli.Application):
    def main(self, b):
    	if b == "block":
    		block_sites()
    	else:
    		un_block()


if __name__ == "__main__":
    MyApp.run()
