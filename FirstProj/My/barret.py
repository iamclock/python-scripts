#! /usr/bin/env python3










def barret(x, m, b, z):
	#b > 3
	r = 0
	k = 0
	t = m
	while t is not 0:
		t = int(t / 10)
		k += 1
	
	t = pow(b, k+1)
	q_ = int((int(x/pow(b, k-1))*z)/t)
	r1 = x % t
	r2 = q_ * m % t
	if r1 >= r2:
		r_ = r1 - r2
	else:
		r_ = t + r1 - r2
	while r_ >= m:
		r_ -= m
	r = r_
	return r








b = 10
x = 1234
m = 20
print("m = "+str(bin(m)))
n = k = 0
t = m

while t is not 0:
	t = int(t / b)
	k += 1
print("k = "+str(k))

z = int(pow(b, 2*k)/m)
print("z = "+str(z))



res = barret(x, m, b, z)

print(res)




