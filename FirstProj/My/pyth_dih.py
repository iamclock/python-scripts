#! /usr/bin/python3




import random


def dihotom(x, y, m):
	q = x
	z = 1
	while y:
		if y&1:
			z = z*q % m
			print("L6= "+str(hex(z))[:2]+str(hex(z))[2:].upper())
		q = q*q % m
		print("L5= "+str(hex(q))[:2]+str(hex(q))[2:].upper())
		y = y >> 1
	return z


x = 0x43c91c949e28da09b4f35475121e7a303e38c2637d1a3d45563030b6d8b65354e66d
y = 0x66883960800969b014af3cf1bf37cf33bb46104aec61853f823325
m = 0x17e9548cf7b998121632002859ef7609ed29eb4deae8ee78f60d3595762897de
z = dihotom(x,y,m)

_z = str(hex(z))

print(_z[:2]+_z[2:].upper())