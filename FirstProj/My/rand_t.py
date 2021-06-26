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
	
	rand_val1 = random.getrandbits(5+i*7)
	rand_val2 = random.getrandbits(5+i*4)
	
	file_dat.write('0'+'x'+str(hex(rand_val1))[2:].upper() + '\n' + '0'+'x'+str(hex(rand_val2)+'\n')[2:].upper())
	file_ans.write('0'+'x'+str(hex(rand_val1 % rand_val2))[2:].upper())
	
	#print('0'+'x'+str(hex(rand_val1))[2:].upper())
	#print('0'+'x'+str(hex(rand_val2))[2:].upper())
	#print('0'+'x'+str(hex(rand_val1 % rand_val2))[2:].upper())
	
	
	string = string[0:-len(str(i))]
	file_dat.close()
	file_ans.close()