#! /usr/bin/env python3




def lcg(a, x ,c, m):
	x = (a * x + c) % m
	return x


def gcd(a, b):
	if (a < b):
		t = b
		b = a
		a = t
	r = b
	while r > 0:
		b = r
		r = a % b
		a = b
	print("gcd = " + str(b))

def gen_lcg():
	#x = 10
	#a = 2
	#c = 3
	#m = 5

	x = 10
	a = 3
	c = 7
	m = 16

	x = 10
	a = 5
	c = 7
	m = 53 # 52
	
	x = 12
	a = 11
	c = 7
	m = 13

	for i in range(0, m):
		x = lcg(a, x, c, m)
		print(x)




gen_lcg()
#gcd(4, 52)