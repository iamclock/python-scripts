'''
Created on 4 июл. 2021 г.

@author: iamclock
'''
from My.First.Stepik import second

# 	(x if x % 2 else None for x in items)

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

# def update_dictionary(d, key, value):
def second():
	d = {}
	key = 1
	value = -1
	k2, k_or_k2 = 2*key, 0
	for x in d:
		if x == key: k_or_k2 |= 1
		if x == k2: k_or_k2 |= 2
	if k_or_k2&1: d[key] += [value]
	elif k_or_k2&2: d[k2] += [value]
	else: d[k2] = [value]
	return 0

def second_alt1():
	d = {}
	key = 1
	value = -1
	key <<= key not in d
	d[key] = d.get(key, []) + [value]
	return 0

def second_alt2():
	d = {}
	key = 1
	value = -1
	try: 
		d[key].append(value)
	except:
		d.setdefault(key*2,[]).append(value)
	return 0

def second_alt3():
	d = {}
	key = 1
	value = -1
	if key in d:
		d[key] = d[key] + [value]
	else:
		d[2 * key] = d.get(2 * key, []) + [value]
	return 0

'''
a aa abC aa ac abc bcd a
########################
a A a
'''
def third():
# 	words = [x.lower() for x in input().split()] # upper()
	dic = {}
	for word in input().lower().split():
		dic[word] = dic.get(word) + 1 if dic.get(word) else 1
	for key in dic:
		print(key, dic[key])
	return 0

def third_alt1():
	s = input().lower().split()
	for i in set(s):
		print(i, s.count(i))
	return 0

def third_alt2():
	x = [i for i in input().lower().split()]
	a = {i:x.count(i)for i in x}
	for i,j in a.items():
		print(i,j)
	return 0

def third_alt3():
	text = input().lower().split()
	d = { i : text.count(i) for i in text  }
	for key, value in d.items():
		print(key, value, end='\n')
	return 0

def third_alt4():
	from collections import Counter
	for i,j in Counter(input().lower().split(' ')).items():
		print(i,j)
	return 0

def third_alt5():
	w = input().lower().split()
	print(*['%s %s' %(x, w.count(x)) for x in set(w)], sep='\n')
	return 0

def third_alt6():
	l = input().lower().split()
	d  = {e:0 for e in l}
	for key in l: d[key]+= 1
	for key,value in d.items(): print(key, value)
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
# 	first()
# 	second()
	third()
	
	
	pass