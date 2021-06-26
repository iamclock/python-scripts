#! /usr/bin/python3




import random



for i in range (34, 40):
	if(i < 10):
		string = "00"
	else:
		string = "0"
	string += str(i)+".dat"
	file_dat = open(string, "wt")
	string = string[0:-4]
	string = string+".ans"
	file_ans = open(string, "wt")
	
	rand_val1 = random.getrandbits(260)
	string = str(hex(rand_val1))
	
	file_dat.write(string+'\n')
	file_ans.write(string[0]+string[1]+string[2:].upper()+'\n')
	
	#string = string[0:-len(str(i))]
	file_dat.close()
	file_ans.close()
