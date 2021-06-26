
def dihotom(x, y, m):
	q = x
	z = 1
	while y:
		print("L5= "+str(hex(q))[:2]+str(hex(q))[2:].upper())
		if y&1:
			z = z*q % m
			print("L6= "+str(hex(z))[:2]+str(hex(z))[2:].upper())
		q = q*q % m
		y = y >> 1
	return z


x = 0x4D908CAEF888
y = 0x17B07
m = 0xA28

print hex(dihotom(x,y,m))
