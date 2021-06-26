#! /usr/bin/env python3


def GCD(x, y):
	if x < y:
		r = y
		y = x
		x = r
	while x > 1:
		r = x % y
		x = y
		y = r
	return x


def main():

	x = a = eval(input("a = "))
	c = eval(input("c = "))
	m = eval(input("m = "))


	# print("a = " + str(a) + "\nx = " + str(x) + "\nc = " + str(c) + "\nm = " + str(m))

	print("GCD(c, m) = " + str(GCD(a, m)))
	print("b = a-1 = " + str(a-1))
	print("")



	step = 0
	print(str(step) + ". " + str(x))
	x = (a*x + c) % m
	while x != a:
		step = step+1
		print(str(step) + ". " + str(x))
		x = (a*x + c) % m
	print("period = " + str(step+1))




print(GCD(4, 7))




