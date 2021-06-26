#! /usr/bin/python3




import random


for i in range (1, 65):
	if(i < 10):
		string = "00"
	else:
		string = "0"
	string += str(i)+".dat"
	file_dat = open(string, "wt")
	string = string[0:-4]
	string = string+".ans"
	file_ans = open(string, "wt")
	
	
	
	rand_val1 = random.getrandbits(i*21+250)
	rand_val2 = random.getrandbits(i*18+200)
	rand_module = 0
	while rand_module == 0:
		rand_module = random.getrandbits(i*3+170)
	
	
	
	print(hex(rand_val1))
	print(hex(rand_val2))
	print(hex(rand_module))
	
	file_dat.write(str(hex(rand_val1))+'\n'+str(hex(rand_val2))+'\n'+str(hex(rand_module))+'\n')
	rand_val1 = pow(rand_val1, rand_val2, rand_module)
	print(hex(rand_val1))
	
	file_ans.write('0'+'x'+str(hex(rand_val1))[2:].upper()+'\n')
	
	string = string[0:-len(str(i))]
	file_dat.close()
	file_ans.close()
