#! /usr/bin/python3



x = int(input(), 16)
y = int(input(), 16)
m = int(input(), 16)
if(m == 0):
	print("Error")
else:
	x = pow(x,y,m)
	print(hex(x))
