'''
Created on 4 июл. 2021 г.

@author: iamclock
'''

def sumFromStdin():
	sum_ = 0
	x = int(input())
	while x:
		sum_ +=x
		x = int(input())
	print(sum_)
	return 0

def lcm(x, y):
	r = y
	while r:
		y = r
		r = x % y
		x = y
	return y

def findLcm():
	x,y = int(input()),int(input())
	print(x*y//lcm(x,y))
	return 0

def thirdteenth():
	op1,op2,met = (input() for _ in range(3))
	op1,op2 = float(op1),float(op2)
	if met == "div":
		try:
			print(op1//op2)
		except ZeroDivisionError:
			print("Деление на 0!")
# 			sys.exit(0)
	elif met == "mod":
		try:
			print(op1 % op2)
		except ZeroDivisionError:
			print("Деление на 0!")
# 			sys.exit(0)
	elif met == '/':
		try:
			print(op1/op2)
		except ZeroDivisionError:
			print("Деление на 0!")
# 			sys.exit(0)
	elif met == "pow":
		print(pow(op1, op2))
	elif met == '+':
		print(op1 + op2)
	elif met == '-':
		print(op1 - op2)
	elif met == '*':
		print(op1 * op2)
	return 0


def thirdteenth_alt():
	first = float(input())
	second = float(input())
	action = input()
	operations = {"mod": "%", "div": "//", "pow": "**"}
	try:
		print(eval("(" + str(first) + ")" + operations.get(action, action) + str(second)))
	except ZeroDivisionError:
		print('Деление на 0!')
	##
	a, b = float(input()), float(input())
	print({
	'+':   a + b,
	'-':   a - b,
	'*':   a * b,
	'/':   a / b if b != 0 else "Деление на 0!",
	'mod': a % b if b != 0 else "Деление на 0!",
	'pow': a ** b,
	'div': a // b if b != 0 else "Деление на 0!"
	}[input()])
	return 0


def matrix():
	n = []
	m = []
	for _ in range(2): n.append(int(input()))
	for _ in range(2): m.append(int(input()))
	n = list(dict.fromkeys(n))
	m = list(dict.fromkeys(m))
	print(' ', end='\t')
	for j in range(m[0], (m[-1]+1)):
		print(j, end='\t')
	for i in range(n[0], (n[-1]+1)):
		print('\n', i, end='\t')
		for j in range(m[0], (m[-1]+1)):
			print(i*j, end='\t')
	return 0

def matrix_alt():
	a=int(input())
	b=int(input())
	c=int(input())
	d=int(input())
	
	print('\t', *range(c, d+1), sep='\t')
	for i in range(a,b+1):
		print(i, *range(i*c,(i*d)+1, i), sep='\t')
	return 0

def fourteenth():
	a,b = int(input()), int(input())
	a += -a%3
	b -= b%3
	print((a+b)/2)
	return 0

def fifteenth():
	s = input()
	count = 1
	cur = None
	for i,cur in enumerate(s[:-1]):
		if cur == s[i+1]: count += 1
		else:
			print(cur, count, end='', sep='')
			count = 1
	print(s[-1], count, end='', sep='')
# 	prev = cur
	return 0

# 4 -1 9 3
# calculating sum of numbers from input
def sixteenth():
# 	sum = 0
# 	for i in input().split():
# 		sum += int(i)
# 	print(sum)
	print(sum(int(i) for i in input().split()))
	return 0

# ! 1 3 5 6 10
# ! 10
# calculating sum of neighbor elements of array from input
def seventeenth():
	seq = [int(i) for i in input().split()]
	m = len(seq)
	if m > 1:
		[print(seq[(i-1)%m]+seq[(i+1)%m], end=' ') for i in range(m)]
	else:
		print(seq[0])
	return 0

# ! 4 8 0 3 4 2 0 3
# ! 10
# ! 1 1 2 2 3 3
# ! 1 1 1 1 1 2 2 2
# output elements from input that meets twice
def eightteenth():
	seq = list([int(i) for i in input().split()])
	seq.sort()
	[print(seq[i], end=' ') for i in range(len(seq)) if seq[i:].count(seq[i]) == 2]
	return 0

'''
1
-3
5
-6
-10
13
4
-8
'''
def nineteenth():
	sum_, sumOfSquares = 0, 0
	while True:
		x = int(input())
		sum_ += x
		sumOfSquares += x*x
		if not sum_: break
	print(int(sumOfSquares))
	return 0

# 7
def twentieth():
	n = int(input())
	l = 0
	if not n: print(n)
	for i in range(n+1):
		for j in range(i):
			if l > n-1: break
			print(i, end=' ')
			l += 1
	return 0

def twentieth_alt():
	n = int(input())
	a = []
	i = 0
	while len(a) < n:
		a += [i] * i
		i += 1
	print(*a[:n])
	return 0

'''
5 8 2 7 8 8 2 4
8
'''
'''
5 8 2 7 8 8 2 4
10
'''
# Вывод индексов искомого объекта
def twentyfirst():
	lst, x = input().split(), input()
	is_found = False
	for i,val in enumerate(lst):
		if x == val:
			is_found = True
			print(i, end=' ')
	if not is_found:
		print("Отсутствует")
	return 0

def twentyfirst_alt():
	l, n = [int(i) for i in input().split()], int(input())
	print(*[x for x in range(len(l)) if l[x]==n] if n in l else ["Отсутствует"])
	##
	##
	lst, x = [int(i) for i in input().split()], int(input())
	if x not in lst:
		print("Отсутствует")
	else:
		[print(i, end=" ") for i, l in enumerate(lst) if l == x]
	##
	##
	lst, x = map(int, input().strip().split()), int(input())
	idx = [i for i, e in enumerate(lst) if e == x]
	print(*idx) if idx else print("Отсутствует")
	return 0

if __name__ == '__main__':
	pass
# 	thirdteenth()
# 	matrix()
# 	fifteenth()
#  	sixteenth()
#  	seventeenth()
# 	eightteenth()
# 	nineteenth()
# 	twentieth()
	twentyfirst()
	
	
	
	
	
	
	
	
	
	
	
	
	