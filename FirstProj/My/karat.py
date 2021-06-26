#! /usr/bin/env python3

# http://samos-it.com/posts/recursive-karatsuba-multiplication-python.html
# http://life-prog.ru/view_teorinfo.php?id=6

from math import ceil


def karat(u, v, b):
	
	n1 = len(str(u))
	n2 = len(str(v))
	
	print("n1 = "+str(n1))
	print("n2 = "+str(n2))
	
'''
	t = u
while t is not 0:
	t = int(t/b)
	n1 += 1

t = v
while t is not 0:
	t = int(t/b)
	n2 += 1
#print("n1 = "+str(n1))
#print("n2 = "+str(n2))
'''
	if n1 > n2:
		n = n1
	else:
		n = n2
	t = n / 2
	
	 = 
	 = 
	ac = karat()
	bd = karat()
	ad_bc = karat((a + b),(c + d)) - ac - bd
	
	
	t = int(ceil(n / 2.0))
	
	if n % 2 is not 0:
		n += 1
	res = ((b ** n) * ac) + ((10 ** t) * ad_bc) + bd
	return res





b = 10
n = 4
u = 25
v = 14


karat(u, v, b)
