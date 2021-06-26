#! /usr/bin/python3




import random


def dihotom(x, y, m):
	q = x
	if y&1:
		z = x
	else:
		z = 1
	y = y >> 1
	while y:
		q = q*q % m
		print("L6= "+str(hex(q))[:2]+str(hex(q)).upper()[2:])
		if y&1:
			z = z*q % m
			print("L5= "+str(hex(z))[:2]+str(hex(z)).upper()[2:])
		y = y >> 1
	return z



x = 0xe92593c7d74c93b4
y = 0x1ffffffffffffffffffffff

x = x%y

z = dihotom(x, y, y)


print("Experiment #1")
print(str(hex(x))[:2]+str(hex(x)).upper()[2:])
print(str(hex(z))[:2]+str(hex(z)).upper()[2:])