# -*- coding: utf-8 -*-
from string import digits, ascii_uppercase

setOfSymbols = ascii_uppercase + digits
begin = 0
end = 64


def print_value(cur_place, cur_state):
	for char in setOfSymbols:
		new_state = cur_state+char
		print_value(cur_place+1, new_state) if(cur_place < (end-1)) else print(new_state)

if __name__ == "__main__":
	'''
	Заполнение словаря значениями для подбора грубой силой
	Начальное состояние задаётся аргументами функции print_value, которая вызывается рекурсивно.
	Если известны первые несколько символов, то следует поместить их в строку и передать аргументом в cur_state, а cur_place, соответственно, указать на следующий символ после известной последовательности
	Порядок нумеруется с 0, тоесть, если известен первый символ, то следующий за ним находится на позиции 1
	'''
	print_value(1, "A")