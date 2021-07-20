'''
Created on 4 июл. 2021 г.

@author: iamclock
'''

# 	(x if x % 2 else None for x in items)


def first(l):
	'''
	Удаление нечётных элементов из списка, изменение чётных делением в два раза
	'''
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
	'''
	
	'''
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
	'''
	
	'''
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

def third_alt7():
	dic = {}
	for i in input().lower().split():
		dic[i] = dic.get(i, 0) + 1
	for key, value in dic.items():
		print(key, value)
	return 0

def third_alt8():
	s = input().lower().split()
	print(*[f'{w} {s.count(w)}' for w in set(s)], sep='\n')
	return 0

def fourth():
	'''
	
	'''
	dic = {}
	for _ in range(int(input())):
		x = int(input())
		if not dic.get(x):
			dic[x] = f(x)
		print(dic[x])
	return 0

def fourth_alt1():
	x = [int(input()) for _ in range(int(input()))]
	b = {x : f(x) for x in set(x)}
	print (*[b[i] for i in x], sep='\n')
	return 0

def fifth():
	'''
	
	'''
	import os
	fpath, fname = '.', 'dataset_3363_2.txt'
	with open(os.path.join(fpath, fname), "r") as inf:
		for line in inf:
			line = line.strip()
			prev_symb, count = None, 0
			for symb in line:
				if '/' < symb < ':':
					count = count*10 + int(symb)
				else:
					print(prev_symb * count, sep='', end='') if prev_symb else None 
					prev_symb = symb
					count = 0
			print(prev_symb * count)
	return 0

def fifth_alt1():
	import re
	with open('dataset_3363_2.txt', "r") as input_s:
		a = re.split('(\d+)', input_s.readline())
		b = (''.join(i[1] * int(i[0]) for i in zip(a[1::2], a[::2])))
		with open("3.4.3.txt", "w") as out_s:
			out_s.write(b)
	return 0

def fifth_alt2():
	s, d = input(), []
	for i in s:
		if not i.isdigit(): d.append(i)
		else: d[-1] += i
	print(*[i[0]*int(i[1:]) for i in d], sep='')
	return 0

def fifth_alt3():
	with open('dataset_3363_2.txt', 'r') as f:
		s = f.readline().strip()
	i = 0
	while i < len(s):
		j = i + 1
		while j < len(s) and s[j].isdigit():
			j += 1
		print(s[i] * int(s[i+1:j]), end='')
		i = j
	return 0

def fifth_alt4():
	
	return 0

def sixth():
	'''
	
	'''
	import os
	fpath, fname = '.', 'dataset_3363_3.txt'
	counter = {}
	with open(os.path.join(fpath, fname), "r") as inf:
		resMax, resWord = 0, None
		for line in inf:
			line = line.split()
			for word in line:
				counter[word] = counter.get(word) + 1 if counter.get(word) else 1 
				if counter[word] > resMax or (counter[word] == resMax and (resWord == None or word < resWord)):
					resWord = word
					resMax = counter[word]
		print(resWord.upper(), resMax)
# 		for i in counter: print(i, counter[i])
	return 0

# Not Work
def sixth_alt1():
	import os
	fpath, fname = '.', 'dataset_3363_3.txt'
	with open(os.path.join(fpath, fname), "r") as inf:
		e, max_,  = ' ', 0
		for line in inf:
			line_length = len(line)
			line = sorted(line.split())
			for i in range(line_length):
				count, j = 1, i+1
				# требуется проверят все оставшиеся элементы с текущим (line[i] до line[n-1]), а не только несколько
				# функция sorted требуется для выполнения требования вывода в лексикографическом порядке 
				while j < line_length and line[i].lower() == line[j].lower():
					count += 1
					j += 1
				if count > max_:
					e, max_, i, count = line[i], count, j, 0
			print(e, max_, sep=' ')
	return 0

def sixth_alt2():
	s = open('file').read()
	s = s.lower().split()
	dic = {i: s.count(i) for i in s}
	v = list(dic.values())
	k = list(dic.keys())
	print(k[v.index(max(v))] + ' ' + str(max(v)))
	return 0

def sixth_alt3():
	with open('dataset_xxx.txt') as file:
		dct = {}
	for line in file:
		lst = [i.lower() for i in line.strip().split()]
		for i in lst:
			dct.update({i: int(dct.get(i, 0)) + 1})
	m = max(dct, key=(lambda key: dct[key]))
	print(m, dct[m])
	return 0

def seventh():
	'''
	
	'''
	import os
	fpath, fname = '.', 'dataset_3363_4.txt'
	foutpath, foutname = '.', 'seventh.txt'
	math, phys, russ, count = 0, 0, 0, 0
# 	with open("file.txt", "r", encoding='utf-8') as file:
	with open(os.path.join(fpath, fname), "r") as inf, open(os.path.join(foutpath, foutname), "w") as outf:
		for line in inf:
			count += 1
			line = line.strip().split(';')
			math += int(line[1])
			phys += int(line[2])
			russ += int(line[3])
# 			print("{}".format( (int(line[1]) + int(line[2]) + int(line[3]))/3 ))
			outf.write("{}\n".format( (int(line[1]) + int(line[2]) + int(line[3]))/3 ))
		outf.write("{:.9f} {:.9f} {:.9f}".format(math/count, phys/count, russ/count))
# 	print("{:.9f} {:.9f} {:.9f}".format(math/count, phys/count, russ/count))
	return 0

def seventh_alt1():
	st = [x.split(';') for x in open('fl.txt').readlines()]
	print(*[sum([int(y) for y in x[1:]])/3 for x in st], sep='\n')
	print(*[sum([int(y) for y in [st[x][z] for x in range(len(st))]])/len(st) for z in range(1,4)])
	return 0

def seventh_alt2():
	import pandas as pd
	df = pd.read_csv('dataset_3363_4.txt', sep=';', names=['Фамилия','Математика', 'Физика', 'Русский язык'])
	mat = df['Математика'].mean()
	phis = df['Физика'].mean()
	rus = df['Русский язык'].mean()
	df['Среднее ученика'] = (df['Математика'] + df['Физика'] + df['Русский язык']) / 3
	mean_learn = df['Среднее ученика']
	with open('result.txt', 'w') as file:
		for value in mean_learn:
			file.write(str(value)+'\n')
		file.write(str(mat)+' '+str(phis)+' '+str(rus))
	return 0

def seventh_alt3():
	s = [0, 0, 0]
	n = 0
	with open('111.txt') as f:
		for line in f:
			m = list(map(int, line.strip().split(';')[1:]))
			print(sum(m)/3)
			for i in 0, 1, 2: s[i] += m[i]
			n += 1
		print(s[0]/n, s[1]/n, s[2]/n)
	return 0

def seventh_alt4():
	import sys
	import statistics
	f = sys.stdin
	l = [list(map(float, l.strip().split(";")[1:])) for l in f]
	print(*[statistics.mean(s) for s in l], sep="\n")
	print(*[statistics.mean(i) for i in zip(*l)])
	return 0

def seventh_alt5():
	students, * points = 0, 0, 0, 0
	with open(r"C:\Users\User\AppData\Local\Temp\dataset_3363_4.txt") as inf, \
	open(r"C:\Users\User\AppData\Local\Temp\out_3363_4.txt", 'w') as ouf:
		for line in inf:
			students += 1
			pts = [int(line.split(';')[i]) for i in (1,2,3)]
			for i in range(3):
				points[i] += pts[i]
			ouf.write(f"{sum(pts)/3}\n")
		ouf.write(f"{' '.join([str(p / students) for p in points])}")
	return 0

def eighth():
	'''
	подсчёт окружности круга
	'''
	from math import pi
	print(pi*2*float(input()))
	return 0

def eighth_alt1():
	from math import tau
	print(tau*2*float(input()))
	return 0

def nineth():
	'''
	вывод только аргументов вызванной программы
	'''
	from sys import argv
	print(*argv[1:])
	return 0

def tenth():
	'''
	Подсчёт строк в скачанном файле
	'''
	from requests import get
	from os import path
	fpath, fname = '.', 'dataset_3378_2.txt'
	with open(path.join(fpath, fname), "r") as inf: resp = get( inf.read().strip() )
	print(len(resp.text.splitlines()))
	return 0

def tenth_alt1():
	import requests
	with open('dataset_3378_2.txt', "r") as inf: r = requests.get(inf.readline().strip())
	print(len(r.text.splitlines()))
	return 0

def tenth_alt2():
	from requests import get
	with open('datasets\dataset_3378_2.txt', "r") as inf: resp = get( inf.read().strip() )
	resp.text.count('\n')
	return 0

# Поиск файла с текстом, из файлов с ссылками на другие файлы с ссылками 
def eleventh():
	'''
	
	'''
	from requests import get
	from os import path
	fpath, fname = '.', 'dataset_3378_3.txt'
	url = "https://stepic.org/media/attachments/course67/3.6.3/" 
	with open(path.join(fpath, fname), "r") as inf:
		resp = get( inf.read().strip() )
	while "We" not in resp.text[:2]:
		resp = get( url + resp.text.strip() )
		print('.', end='', sep='')
	print('\n' + resp.text)
	return 0

def eleventh_alt1():
	import requests
	url, name = 'https://stepic.org/media/attachments/course67/3.6.3/', '699991.txt'
	while name[:2] != 'We':
		name = requests.get(url + name).text
	print(name)
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
# 	third()
# 	fifth()
# 	sixth()
# 	seventh()
# 	tenth()
	eleventh()
	
	
	pass