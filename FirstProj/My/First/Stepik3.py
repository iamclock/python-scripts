'''
Created on 4 июл. 2021 г.

@author: iamclock
'''

'''
Удаление нечётных элементов из списка, изменение чётных делением в два раза
'''
def first(l):
# 	l = [1, 3, 7]
# 	l = [1, 2, 3, 4, 5, 6, 7]
	n = len(l)
	# reversed не создаёт копию списка
	for i,e in enumerate(reversed(l)):
		if not (e%2): l[n-i-1] //= 2
		else: l.remove(e)
		print(*l)
	
	return 0

def first_alt1(l):
	b = []
	for x in l:
		if x % 2 == 0:
			b.append(x // 2)
	l[:] = b
	return 0

def first_alt2(l):
	for i in reversed(range(len(l))):
		if l[i] % 2 == 1:
			del l[i]
		else:
			l[i] //= 2
	return 0

def first_alt3(l):
	l[:] = [i//2 for i in l if not i % 2]
	return 0

def first_alt4(l):
	for x in l[:]:
		if not x % 2:
			l.append(x//2)
		l.remove(x)
	return 0

def first_alt5(l):
	return 0

def temp1():
	return 0

def temp2():
	return 0

def temp3():
	return 0

def temp4():
	return 0

def temp5():
	return 0

def temp6():
	return 0

def temp7():
	return 0

def temp8():
	return 0

def temp9():
	return 0

def temp10():
	return 0

def temp11():
	return 0

def temp12():
	return 0

def temp13():
	return 0

def temp14():
	return 0

def temp15():
	return 0


if __name__ == '__main__':
	first()
	
	pass