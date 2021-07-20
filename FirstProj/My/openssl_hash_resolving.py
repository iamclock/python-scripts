'''
Created on 20 июл. 2021 г.

@author: iamclock
'''
#! /usr/bin/env python3

import subprocess


passwds = ["admin", "Admin"]
part = "SqBiqAirTgYvWhEd.s4ve+heW0r1dhaWyE3gHz"
salt = "Qui.P1zz49OM4sterX3y"

for word in passwds:
	outp = subprocess.run("openssl passwd -6 -salt {} {}".format(salt, word), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	if part in str(outp.stdout):
		print("{}: {}".format(word, outp.stdout))
		break