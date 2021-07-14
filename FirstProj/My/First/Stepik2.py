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

def first():
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


def first_alt():
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

def second():
	a,b = int(input()), int(input())
	a += -a%3
	b -= b%3
	print((a+b)/2)
	return 0

def third():
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
def fourth():
# 	sum = 0
# 	for i in input().split():
# 		sum += int(i)
# 	print(sum)
	print(sum(int(i) for i in input().split()))
	return 0

# ! 1 3 5 6 10
# ! 10
# calculating sum of neighbor elements of array from input
def fifth():
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
def sixth():
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
def seventh():
	sum_, sumOfSquares = 0, 0
	while True:
		x = int(input())
		sum_ += x
		sumOfSquares += x*x
		if not sum_: break
	print(int(sumOfSquares))
	return 0

# 7
def eighth():
	n = int(input())
	l = 0
	if not n: print(n)
	for i in range(n+1):
		for j in range(i):
			if l > n-1: break
			print(i, end=' ')
			l += 1
	return 0

def eighth_alt():
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
def nineth():
	lst, x = input().split(), input()
	is_found = False
	for i,val in enumerate(lst):
		if x == val:
			is_found = True
			print(i, end=' ')
	if not is_found:
		print("Отсутствует")
	return 0

def nineth_alt():
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


'''
9 5 3
0 7 -1
-5 2 9
end
###############
1
end
'''
def tenth():
	matr, x = [], input()
	while 'end' not in x:
		matr.append([int(i) for i in x.split()])
		x = input()
	
	mLength, strLength = len(matr), len(matr[0])
# 	curObjNeighSum = 0
	for i in range(mLength):
		for j in range(strLength):
# 			if j+1 > strLength-1: curObjNeighSum += matr[i][0]
# 			else: curObjNeighSum += matr[i][j+1]
# 			
# 			if j-1 < 0: curObjNeighSum += matr[i][strLength-1]
# 			else: curObjNeighSum += matr[i][j-1]
# 			
# 			if i+1 > mLength-1: curObjNeighSum += matr[0][j]
# 			else: curObjNeighSum += matr[i+1][j]
# 			
# 			if i-1 < 0: curObjNeighSum += matr[mLength-1][j]
# 			else: curObjNeighSum += matr[i-1][j]
			print(	matr[i][j-1] + matr[i][j+1-strLength] + 
					matr[i-1][j] + matr[i+1-mLength][j],
					end=' ')
# 			curObjNeighSum = 0
		print()
	
	# for i in matr: print(*i)
	return 0

# сохранил на будущее метод обхода массива 
def eleventh_trash():
	for i in (i for i in (range(1,(n >> 1))) if i < j):
		matr[i], matr[j] = matr[j], matr[i]
		i += 1
		j -= 1
	return 0

#Вывод матрицы спиралью
'''
5
1 2 3 4 5
16 17 18 19 6
15 24 25 20 7
14 23 22 21 8
13 12 11 10 9
'''
def eleventh():
	n = 5 #int(input())
	matr = [[0]*n for i in range(n)]
	offset = 0
	curSide = n
	l = 1
	while offset < (n/2):
		print(offset, curSide)
		for i in range(curSide):
			matr[offset][offset+i] = l
			l += 1
		
		print("first")
		print(*[matr[i] for i in range(n)], sep='\n')
		print()
		
		for i in range(curSide-2):
			matr[1+offset+i][n-offset-1] = l
			l += 1
		
		print("second")
		print(*[matr[i] for i in range(n)], sep='\n')
		print()
		
		if (n//2 - offset) > 0:
			for i in range(curSide):
				matr[n-1-offset][n-offset-1-i] = l
				l += 1
		
		print("third")
		print(*[matr[i] for i in range(n)], sep='\n')
		print()
		
		for i in range(curSide-2):
			matr[n-2-offset-i][offset] = l
			l += 1
		
		print("fourth")
		print(*[matr[i] for i in range(n)], sep='\n')
		print()
		
		offset += 1
		curSide -= 2
	
	# print(*[matr[i] for i in range(n)], sep='\n')
	for i in range(n): print(*matr[i])
	return 0



def eleventh_alt1():
	n=int(input())
	t=[[0]*n for i in range (n)]
	i,j=0,0
	for k in range(1, n*n+1):
		t[i][j]=k
		if k==n*n: break
		if i<=j+1 and i+j<n-1: j+=1
		elif i<j and i+j>=n-1: i+=1
		elif i>=j and i+j>n-1: j-=1
		elif i>j+1 and i+j<=n-1: i-=1
	for i in range(n):
		print(*t[i])
	return 0

def eleventh_alt2():
	x,i,j=1,0,0; n=int(input())
	a=[[0]*n for i in range (n)]
	a[n//2][n//2]=n**2
	for s in range (n//2):
		for rotate in range (4):
			for j in range (n-1-s*2):
				a[i+s][j+s]=x
				x=x+1
			a=[[a[i][j] for i in range(n)] for j in range (n-1,-1,-1)]
	for i in a:
		print(*i)
	return 0

def eleventh_alt3():
	n = int(input())
	m = [[0] * n for i in range(n)]
	i, j, di, dj = 0, 0, 0, 1
	for k in range(n * n):
		m[i][j] = k + 1
	if (not -1 < i + di < n) or (not -1 < j + dj < n) or m[i + di][j + dj] != 0:
		di, dj = dj, -di
	i, j = i + di, j + dj
	[print(*i) for i in m]
	return 0

def eleventh_alt4():
	n = int(input())
	m = [[0 for i in range(n)] for j in range(n)]
	for k in range(n, 0, -1): 
		for j in range(n-k, k):
			m[n-k][j] = m[n-k][j-1] + 1
		for i in range(n-k, k-1): 
			m[i+1][k-1] = m[i][k-1] + 1    
		for j in range(k-2, n-k-1, -1):
			m[k-1][j] = m[k-1][j+1] + 1     
		for i in range(k-2, n-k, -1): 
			m[i][n-k] = m[i+1][n-k] + 1
		for i in m:
			print(*i)
	return 0

def eleventh_alt5():
	n = int(input())
	for i in range (n):
		for j in range(n):
			k = min (i, j, n - i - 1, n - j - 1)
			if i <= j:
				print (4 * k * (n - k) + j - k + i - k + 1, end = ' ')
			else:
				print (2 * (2 * (n - 2 * k) - 1) + 4 * k * (n - k) - (j - k + i - k + 1), end = ' ')
		print()
	return 0

def eleventh_alt6():
	n = int(input())
	num = [[0] * n for y in range(n)]
	y, x, dy, dx = 0, 0, 0, 1
	
	for k in range(n*n):
		num[y][x] = k+1
		if (y+dy not in range(-1,n)or    #не столбец
			x+dx not in range(-1,n)or    #не строка
			num[y + dy][x + dx] > 0):    #следующая занята
				dx, dy = -dy, dx              #то - переприсваивание
		y, x = y + dy, x + dx
	
	[print(*i) for i in num]
	return 0

# Инициализировать матрицу нулями
def cr_clean_matrix():
	n = 5
	matr1 = [[0]*n for i in range(n)]
	matr2 = [[0 for i in range(n)] for j in range(n)]
	return 0


if __name__ == '__main__':
	pass
	