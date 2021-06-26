'''

Created on 26 июн. 2021 г.

@author: Bourne
'''

def first():
	print("first")
	return 0


def second():
	x = 5
	y = 10
	print(y > x * x or y >= 2 * x and x < y)
	return 0


'''
Sample Input 1:

6
10
8
Sample Output 1:

Это нормально
Sample Input 2:

7
9
10
Sample Output 2:

Пересып
Sample Input 3:

7
9
2
Sample Output 3:

Недосып
'''

def third():
	a, b, h = (int(input()) for _ in range(3))
# 	print('Недосып'*(h < a) + 'Пересып'*(h > b) + 'Это нормально'*((a-1) < h and (b+1) > h))
	print("Недосып" if h < a else "Пересып" if h > b else "Это нормально")
# 	print(("Недосып", "Это нормально", "Пересып")[(h > b) - (h < a) + 1])
	return 0

def fourth():
	x = int(input())
	print("Високосный" if (  ( x%100 and (not x%4) ) or (not x%400) ) else "Обычный")
# 	exec("print( 'Високосный' if ( not {0}%4 and {0}%100 ) or ( not {0}%400 ) else 'Обычный' )".format(int(input())))
	return 0

def fifth(a, b, c): # gerron
# 	a, b, c = (int(input()) for _ in range(3))
	p = (a + b + c)/2
	return( (p * (p-a) * (p-b) * (p-c))**0.5 )
# 	exec("print(((({0}+{1}+{2})/2)*(({0}+{1}+{2})/2-{0})*(({0}+{1}+{2})/2-{1})*(({0}+{1}+{2})/2-{2}))**(1/2))".format(float(input()),float(input()),float(input())))
# 	return 0

def sixth1():
	x = int(input())
	try:
		assert (-15 < x not in [13, 14, 17, 18])
	except AssertionError:
		print(False)
		return 0 # sys.exit(0)
	print(True)
	return 0

def sixth2():
	x = int(input())
	print(x > -15 and not (x in [13, 14, 17, 18]))
	print( (x in range(-14, 13)) or (x in range(15, 17)) or (x >= 19) )
	print((lambda x: (-15 < x < 13) or (14 < x < 17) or x > 18)(int(input())))
	exec("print( {0} > -15 and not ({0} in [13, 14, 17, 18]) )".format(int(input())))
# 	print(-15 < int(input()) not in[13, 14, 17, 18])
	return 0

def seventh():
	a = int(input())
	try:
		b = int(input())
	except ZeroDivisionError:
		print("Деление на 0!")
	
	
	
	return 0

def eighth():
	
	
	
	return 0

def ninth():
	variables = []
	pi, i, S = 3.14, 0, 1
	type_ = input()
	while True:
		variables.append(int(input()))
		i += 1
		if type_ == "круг" and i == 1:
			S = pi*variables[0]**2
			break
		elif type_ == "прямоугольник" and i == 2:
			for x in variables:
				S *= float(x)  
			break
		elif type_ == "треугольник" and i == 3:
			p = (variables[0] + variables[1] + variables[2])/2
			S = (p * (p-variables[0]) * (p-variables[1]) * (p-variables[2]))**0.5 # S = fifth(variables[0], variables[1], variables[2])
			break
	print(S)
	return 0

def ninth2():
	pi = 3.14
	type_ = input()
	if type_ == "круг":
		print(pi*int(input())**2)
	elif type_ == "прямоугольник":
		print(int(input())*int(input()))
	elif type_ == "треугольник":
		a,b,c = int(input()), int(input()), int(input())
		p = (a + b + c)/2
		print((p * (p-a) * (p-b) * (p-c))**0.5)
	return 0

def ninth3():
	figure = {'треугольник': [3, lambda a, b, c: ((a+b+c)/2*((a+b+c)/2-a)*((a+b+c)/2-b)*((a+b+c)/2-c))**0.5], 
	          'прямоугольник': [2, lambda a, b: a*b], 
	          'круг': [1, lambda r: 3.14*r**2]}
	f = input()
	print(figure[f][1](*(float(input()) for _ in range(figure[f][0]))))
	return 0

def tenth():
	arr = []
	for i  in range(3):
		arr.append(int(input()));
	arr.sort(reverse=True)
# 	arr[1], arr[2] = arr[2], arr[1]
	arr[1] ^= arr[2]
	arr[2] ^= arr[1]
	arr[1] ^= arr[2]
	for obj in arr:
		print(obj)
	return 0

def tenth_alternatives():
	a, b, c = int(input()), int(input()), int(input())
	max_int = max(a, b, c)
	min_int = min(a, b, c)
	print(max_int)
	print(min_int)
	print((a + b + c) - max_int - min_int)
	##
	arr = []
	for i  in range(3):
		arr.append(int(input()));
	arr.sort(reverse=True)
	print(arr[0], arr[2], arr[1], sep='\n')
	##
	x=sorted([int(input()),int(input()),int(input())])
	print (x[2], x[0], x[1], sep="\n")
	##
	print("{2}\n{0}\n{1}".format(*sorted([int(input()) for i in range(3)])))
	return 0

if __name__ == '__main__':
# 	pass
# 	first()
# 	second()
# 	third()
# 	fourth()
# 	fifth()
# 	sixth1()
# 	seventh()
# 	ninth()
	tenth()
	
	
	
	
	
	
