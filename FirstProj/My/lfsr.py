#! /usr/bin/env python3




def LFSR(reg, poly):
	bit = reg & 1
	reg >>= 1
	if bit:
		reg = reg ^ poly
	return reg, bit


def chk_period():
	#seed = reg = 0x3fffffff
	#poly = 0x200004E1
	#seed = reg = 0xace1
	#poly = 0xb400
	#seed = reg = 0xaffffffff
	#poly = 0x4000006E3
	#seed = reg = 0xffffffff
	#poly = 0x80000A92
	seed = reg = 0x1
	poly = 0x5
	
	period = 0
	print(str(hex(reg)))
	while True:
		reg, bit = LFSR(reg, poly)
		print(bit, end="")
		#print(str(hex(reg)))
		period += 1
		if reg == seed:
			break
	print()
	print(str(hex(reg)))
	print(str(period))
	
	



#def main():
chk_period()

