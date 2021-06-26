#! /usr/bin/python3



import subprocess


str_help = "	show ip route - вывод таблицы маршрутизации\n	show interfaces - вывод информации обо всех сетевых интерфейсах\n	show interface {ethernet | loopback} number - вывод информации о заданном интерфейсе\n	ip route prefix mask ip-address - добавление статического маршрута к сети prefix с маской mask через шлюз ip-address\n	no ip route prefix mask ip-address - удаление статического маршрута\n	interface {ethernet | loopback} number - выбор интерфейса для конфигурирования\n		ip address ip-address mask - задание IP-адреса и сетевой маски для выбранного интерфейса\n		no ip address ip-address mask - удаление IP-адреса и сетевой маски для выбранного интерфейса\n		shutdown - отключение интерфейса\n		no shutdown - включение интерфейса\n	ip name-server server-address1 [server-address2] - задание DNS-сервера\n	no ip name-server server-address1 [server-address2] - удаление DNS-сервера\n	ip routing - включение режима маршрутизации\n	no ip routing - отключение режима маршрутизации\n"


def dict_conc(obj_dict):
	conc = ''
	for element in obj_dict:
		conc += element
	return conc



def mask_wizard(mask):
	numer = 0
	for i in mask:
		if i == "0":
			pass
		elif i == "128":
			numer += 1
		elif i == "192":
			numer += 2
		elif i == "224":
			numer += 3
		elif i == "240":
			numer += 4
		elif i == "248":
			numer += 5
		elif i == "252":
			numer += 6
		elif i == "254":
			numer += 7
		elif i == "255":
			numer += 8
		else:
			return -1
	return numer




def interface(interface, number):
	
	if interface == "loopback":
		inter = "lo"
	else:
		inter = "eth"
	
	check = subprocess.Popen(("ifconfig "+inter+str(number)).split(" "), stdout=subprocess.PIPE)
	
	check = check.stdout.read().decode("utf-8")
	
	if len(check) == 0:
		return
	
	
	while True:
		string = input("router#"+interface+"> ")
		if string == '' or string == "quit" or string == "done":
			if string == "quit" or string == "done":
				break
			pass
		elif string == "shutdown":
			subprocess.call("sudo ifconfig "+inter+str(number)+" down", shell=True)
		elif string == "no shutdown":
			subprocess.call("sudo ifconfig "+inter+str(number)+" up", shell=True)
		else:
			parsed_string = string.split(" ")
			length_parstr = len(parsed_string)
			fail = index = 0
			if parsed_string[index] == "no":
				index += 1
				if length_parstr == 1:
					fail = 1
					print("Command \"no\" must use with arguments. Type help for more information.")
			if fail == 0 and parsed_string[index] == "ip":
				index += 1
				if index < length_parstr and parsed_string[index] == "address":
					index += 1
					if index < length_parstr:
						ip_adr = parsed_string[index].split(".")
						index += 1
						if len(ip_adr) == 4:
							fail = 0
							for i in ip_adr:
								try:
									check_ip_adr = int(i)
								except ValueError:
									fail = 1
									print("Incorrect IP address")
							if fail == 0:
								if index < length_parstr:
									mask = parsed_string[index].split('.')
									index += 1
									if len(mask) == 4:
										for i in mask:
											try:
												check_mask = int(i)
											except ValueError:
												fail = 1
												print("Incorrect mask")
										if fail == 0:
											numb_mask = mask_wizard(mask)
											if numb_mask != -1:
												#print(index)
												if index == 4:
													subprocess.call("sudo ip addr add "+parsed_string[index-2]+"/"+str(numb_mask)+" brd + dev "+inter+str(number), shell=True)
												else:
													subprocess.call("sudo ip addr del "+parsed_string[index-2]+"/"+str(numb_mask)+" dev "+inter+str(number), shell=True)
											else:
												print("Incorrect mask")
									else:
										print("Incorrect mask")
								else:
									print("Need more arguments. Type \"help\" for more information")
						else:
							print("Incorrect IP address")
					else:
						print("Too few arguments for this command. Type \"help\" for more information")
			if index < length_parstr:
				print("Command "+parsed_string[index]+" not found")
	return




req_help = "help"
history = "history"
ip_routing = "ip routing"
no_ip_routing = "no ip routing"


string = None

# Вариант #1
check = subprocess.Popen("cat /proc/sys/net/ipv4/ip_forward".split(" "),  stdout=subprocess.PIPE)
check = check.stdout.read().decode("utf-8")
ipRoutingMode = 2 # сделано здесь для отладки, если cat будет правильно возвращать значение ( 0 или 1) тогда можно убрать, ибо условие ниже будет всегда проходить правильно

if check[0] == '1':
	ipRoutingMode = True
elif check[0] == '0':
	ipRoutingMode = False


'''
Вариант #2
f1 = open('/proc/sys/net/ipv4/ip_forward')
ch = f1.read(1)
if ch == '0':
	ipRoutingMode = False
else:
	ipRoutingMode = True
'''


while True:
	fail = 0
	string = input("router> ")
		
	if string == '' or string == 'off' or string == "quit" or string == "exit":
		if string == 'off' or string == "quit" or string == "exit":
			break
		pass
	elif string == req_help:
		print(str_help)
	else:
		parsed_string = string.split(" ")
		length_parstr = len(parsed_string)
		index = 0
		if parsed_string[index] == "show": # show ip route; show interfaces; show interface {ethernet | loopback} number
			index += 1
			if length_parstr == 1:
				fail = 1
				print("Command \"show\" must use with arguments. Type help for more information.")
		if fail == 0 and index < length_parstr and (parsed_string[index] == "interfaces" or parsed_string[index] == "interface"): #interface {ethernet | loopback} number
			if index == 0 and parsed_string[index] == "interfaces":
				pass
			else:
				index += 1
				if parsed_string[index-1] == "interface":
					few = 1
					if index < length_parstr and (parsed_string[index] == "ethernet" or parsed_string[index] == "loopback"):
						index += 1
						if index < length_parstr:
							few = 0
							try:
								int(parsed_string[index])
							except ValueError:
								print("Incorrect argument. Must be a number")
							else:
								index += 1
								if index == 3: # show interface {ethernet | loopback} number
									if parsed_string[index-2] == "ethernet":
										interface("eth", int(parsed_string[index-1]))
									if parsed_string[index-2] == "loopback":
										interface("lo", int(parsed_string[index-1]))
								else: # interface {ethernet | loopback} number
									inter = "lo"
									if parsed_string[index-2] == "ethernet":
										inter = "eth"
									subprocess.call("ifconfig "+inter+parsed_string[index-1], shell=True)
									index += 1
					if few == 1:
							print("Too few arguments for this command")
					#else:
						#print("Command ", parsed_string[index-1], " not found", sep="")
				elif parsed_string[index-1] == "interfaces":
					if index == length_parstr:
						subprocess.call("ifconfig -a", shell=True)
					else:
						print("Unknown command \""+parsed_string[index]+"\" for \"interfaces\"")
						index += 1
				else:
					print("Command \"interface\" must use with arguments. Type help for more information")
		if index == 0 and parsed_string[index] == "no":
			if length_parstr == 1:
				print("Too few arguments for this command. Type help for more information")
			else:
				index += 1
		if index < length_parstr and parsed_string[index] == "ip":
			index += 1
			condition = 0
			if index < length_parstr:
				if parsed_string[0] == "show":
					if parsed_string[index] == "route":
						index += 1
						if index == length_parstr:
							subprocess.call("netstat -rn", shell=True)
				elif parsed_string[0] == "no":
					if parsed_string[index] == "route":
						# no ip route prefix mask ip-address
						index += 1
						if length_parstr == index + 3:
							#print(parsed_string[index])
							#print(parsed_string[index+1])
							#print(parsed_string[index+2])
							mask = parsed_string[index+1].split(".")
							index += 3
							if len(mask) == 4:
								mask_numb = mask_wizard(mask)
								#print(mask_numb)
								if mask_numb > 1:
									print(parsed_string[0])
									subprocess.call("sudo ip route del "+parsed_string[index-3]+'/'+str(mask_numb)+" via "+parsed_string[index-1], shell=True)
								else:
									print("Incorrect mask")
							else:
								print("Incorrect mask")
						else:
							print("Too few arguments")
					elif parsed_string[index] == "name-server":
						# no ip name-server server-address1 [server-address2] - удаление DNS-сервера
						index += 1
						if index < length_parstr:
							for i in range(index, length_parstr):
								check_dns_serv = parsed_string[i].split(".")
								fail = 0
								for j in check_dns_serv:
									try:
										bryak = int(j)
									except ValueError:
										fail = 1
										print("Incorrect address "+j)
										break
								if fail == 0:
									index = i+1
									'''
									check = subprocess.Popen(("grep "+parsed_string[i]+" /home/porsch/2015/netsbit/test.txt").split(" "), stdout=subprocess.PIPE)
									check = check.stdout.read().decode("utf-8")
									if len(check) == 0:
										print("There is no match in DNS servers list")
									else:
										subprocess.call("sudo grep -v "+parsed_string[i]+" ~/2015/netsbit/test.txt > ~/temp.txt", shell=True)
										subprocess.call("sudo cat ~/temp.txt > ~/2015/netsbit/test.txt", shell=True)
										subprocess.call("rm ~/temp.txt", shell=True)
									'''
									check = subprocess.Popen(("sudo grep "+parsed_string[i]+" /etc/resolv.conf").split(" "), stdout=subprocess.PIPE)
									check = check.stdout.read().decode("utf-8")
									if len(check) == 0:
										print("There is no match in DNS servers list, or file does not exists")
									else:
										subprocess.call("sudo grep -v "+parsed_string[i]+" /etc/resolv.conf > ~/qwerfdctemp.txt", shell=True)
										subprocess.call("sudo cat ~/qwerfdctemp.txt > /etc/resolv.conf", shell=True)
										subprocess.call("rm ~/qwerfdctemp.txt", shell=True)
										#'''
									if i == 6:
											break
								else:
									break
					elif parsed_string[index] == "routing":
						index += 1
						if index == length_parstr:
							if ipRoutingMode == False:
								print("ip routing mode is already off", sep="")
							else:
								echo = subprocess.Popen("echo \"0\"", stdout=subprocess.PIPE, shell=True)
								tee = subprocess.Popen("sudo tee /proc/sys/net/ipv4/ip_forward", stdin=echo.stdout, stdout=subprocess.PIPE, shell=True).wait()
								# команда stdout=subprocess.PIPE используется здесь, для того, чтобы tee не выводила результат на экран, тоесть результаты из потока вывода оседают в объекте tee.
								# метод wait() используется для того, чтобы скрипт ждал ввода кода администратора и не продолжал работу
								print("ip routing mode is off", sep="")
								ipRoutingMode = False
				elif index == 1:
					if parsed_string[index] == "route":
						# ip route prefix mask ip-address
						index += 1
						if length_parstr == index + 3:
							#print(parsed_string[index])
							#print(parsed_string[index+1])
							#print(parsed_string[index+2])
							mask = parsed_string[index+1].split(".")
							index += 3
							if len(mask) == 4:
								mask_numb = mask_wizard(mask)
								#print(mask_numb)
								if mask_numb > 1:
									#print(parsed_string[0])
									subprocess.call("sudo ip route add "+parsed_string[index-3]+'/'+str(mask_numb)+" via "+parsed_string[index-1], shell=True)
								else:
									print("Incorrect mask")
							else:
								print("Incorrect mask")
						else:
							print("Too few arguments")
					elif parsed_string[index] == "name-server":
						#ip name-server server-address1 [server-address2] - задание DNS-сервера
						index += 1
						if index < length_parstr:
							for i in range(index, length_parstr):
								check_dns_serv = parsed_string[i].split(".")
								fail = 0
								for j in check_dns_serv:
									try:
										bryak = int(j)
									except ValueError:
										fail = 0
										print("Incorrect address "+j)
										break
								if fail == 0:
									index = i+1
									'''
									home = subprocess.Popen("echo $HOME", stdout=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")
									command = "grep "+parsed_string[i]+' '+home[:-1]+"/2015/netsbit/test.txt"
									check = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
									#Любая ошибка grepa игнорируется
									error_check = check.stderr.read().decode("utf-8")
									check = check.stdout.read().decode("utf-8")
									if len(check) > 0:
										print(parsed_string[i]+" address is already in list")
									else:
										subprocess.call("sudo echo \'nameserver "+parsed_string[i]+"\' >> ~/2015/netsbit/test.txt", shell=True)
									'''
									check = subprocess.Popen(("sudo grep "+parsed_string[i]+" /etc/resolv.conf").split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
									#Любая ошибка grepa игнорируется
									#error_check = check.stderr.read().decode("utf-8")
									check = check.stdout.read().decode("utf-8")
									if len(check) > 0:
										print(parsed_string[i]+" address is already in list")
									else:
										subprocess.call("sudo echo \'nameserver "+parsed_string[i]+"\' >> /etc/resolv.conf", shell=True)
										#'''
									if i == 6:
											break
								else:
									break
					elif parsed_string[index] == "routing":
						index += 1
						if index == length_parstr:
							if ipRoutingMode == True:
								print("ip routing mode is already on", sep="")
							else:
								echo = subprocess.Popen("echo \"1\"", stdout=subprocess.PIPE, shell=True)
								tee = subprocess.Popen("sudo tee /proc/sys/net/ipv4/ip_forward", stdin=echo.stdout, stdout=subprocess.PIPE, shell=True).wait()
								# команда stdout=subprocess.PIPE используется здесь, для того, чтобы tee не выводила результат на экран, тоесть результаты из потока вывода оседают в объекте tee.
								# метод wait() используется для того, чтобы скрипт ждал ввода кода администратора и не продолжал работу
								print("ip routing mode is on", sep="")
								ipRoutingMode = True
			else:
				if parsed_string[0] == "show":
					print("Too few arguments for \"show\" command. Type help for more information.")
				elif parsed_string[0] == "no":
					print("Too few arguments for this command. Type help for more information.")
		if index < length_parstr:
			print("Command ", parsed_string[index], " not found", sep="")
		#for item in parsed_string:
		#	parsed_string.remove(item)
		
		
		
		
		
		
	'''
	elif string == history:
		for j in history:
			print(history[j],"\n", sep="")
	
	else:
		flag = False
	++i
	sleep(0.01)
	
	if len(parsed_string) > 3:
		print(parsed_string[3])
	'''
	
