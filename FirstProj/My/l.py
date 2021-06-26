#!/usr/bin/python
# -- encoding: utf-8 --
import sys, re, os

# отладочный вывод интерпретатора
def debug(message):
    print("[DEBUG]: %s" % message)
	
# внутренняя ошибка интерпретатора. Необходимо связаться с разработчиком при появлении подобной ошибки
def internal_error(ttt, message):
    print("[INTERNAL ERROR]: %s" % message)
    fd = open('assfile.s', 'w')
    fd.write(ttt)
    fd.close
    sys.exit(1)

# вычисление адреса (смещения в БИМе) объекта name
def getaddr(name):
#	debug(name)
	m = re.match('^[a-z]$', name)
	if m:   # a-z переменные
		adr = (ord(name)-ord('a')+1)*4
	m = re.match('^(L|F|Q|S)(\d+)$', name)
	if m:	# комплексы. L1, L2, F23
		if (int(m.group(2)) < 1) or  (int(m.group(2)) > 99):
			internal_error(name,'номер комплекса не 1 - 99')
		if m.group(1) == 'Q':
			adr = (int(m.group(2))-1)*4+1020
		elif m.group(1) == 'S':
			adr = (int(m.group(2))-1)*4+620
		else:
			adr = (int(m.group(2))-1)*4+220
	m = re.match('^[Z]$', name)
	if m:
		adr = 108
	return adr

def createArray(stext, array_name, size):
	if re.match('^[0-9]+',size):
		perem = 0
	elif re.match('^[a-z]',size):
		perem = 1
	else:
		internal_error(stext,'createArray crash: "%s" емкость - число или переменная - ' % array_name+size)
	index = int(array_name[1:])
	if array_name[0] == 'L':
		bprotect = 0
	elif array_name[0] == 'F':
		bprotect = 1
	else:
		internal_error(stext,'createArray crash: unknow type of array "%s"' % array_name)
	if (index < 100) and (index > 0) :
		adr = int(index) + 120
		stext = stext + '  mov byte[ebp+' + str(adr) + '],' + str(bprotect) + chr(10)
		adr = int(index-1)*4 + 220
		stext = stext + '  mov ebx,[_addrbim]' + chr(10) + '  mov [ebp+' + str(adr) + '],ebx' +  chr(10)
		if perem == 1:
			stext = stext + '  mov eax,[ebp+' + str((ord(size)-ord('a')+1)*4) +  ']\n'
			stext = stext + '  mov [ebp+' + str(adr+400) + '],eax' + chr(10)
			if array_name[0] == 'L':
				stext = stext + '  shl eax,2\n'
			else:
				stext = stext + '  and eax,0xfffffff0\n  add eax,16\n'
			stext = stext + '  add [_addrbim],eax' +  chr(10)
		else:
			if array_name[0] == 'L':
				emc_byte = int(size)*4
			else:
				emc_byte = (int(size)+3)/4*4
			stext = stext + '  mov [ebp+' + str(adr+400) + '],dword ' + str(size) + chr(10)
			stext = stext + '  add [_addrbim],dword ' + str(emc_byte) +  chr(10)
		stext = stext + '  mov [ebp+' + str(adr+800) + '],dword 0' + chr(10)
		stext = stext + '  call _addmem' + chr(10)		
	else:
		internal_error(stext,'createArray crash: номер комплекса должен быть >0 и <100')
#    debug(stext)
	return stext
    
def appendArray(stext, array_name, size):
	if re.match('^[0-9]+',size):
		perem = 0
	elif re.match('^[a-z]',size):
		perem = 1
	else:
		internal_error(stext,'appendArray crash: "%s" емкость - число или переменная - ' % array_name+size)
	index = int(array_name)
	if (index < 100) and (index > 0) :
		adr = int(index-1)*4 + 620
		stext = stext + '  mov ebx,[_addrbim]' + chr(10) + '  mov [ebp+' + str(adr) + '],ebx' +  chr(10)
		if perem == 1:
			stext = stext + '  mov eax,[ebp+' + str((ord(size)-ord('a')+1)*4) +  ']\n'
			stext = stext + '  add [ebp+' + str(adr) + '],eax' + chr(10)
			stext = stext + '  add [_addrbim],eax' +  chr(10)
		else:
			stext = stext + '  add [ebp+' + str(adr) + '],dword ' + str(size) + chr(10)
			stext = stext + '  add [_addrbim],dword ' + str(size) +  chr(10)
		stext = stext + '  call _addmem' + chr(10)		
	else:
		internal_error(stext,'appendArray crash: номер комплекса должен быть >0 и <100')
#    debug(stext)
	return stext
    
def call(stext, name, callsign, functions):
#	nf=name[1:]
	sign = functions[name][0]
#	debug(sign)
#	debug(callsign)
	stext = stext + '  sub esp,1420\n  mov edx,esp\n  mov ecx,1420\n  mov edi,edx\n  xor eax,eax\n  rep stosb\n  push ebp\n'
	invp, outvp = re.split('/', callsign, 1)
	if invp == '':
		invp = []
	else:
		invp = re.split('[\s,]+', invp)
	if outvp == '':
		outvp = []
	else:
		outvp = re.split('[\s,]+', outvp)
	inv, outv = re.split('/', sign, 1)
	if inv == '':
		inv = []
	else:
		inv = re.split('[\s,]+', inv)
	if outv == '':
		outv = []
	else:
		outv = re.split('[\s,]+', outv)
	if len(inv) != len(invp) or len(outv) != len(outvp):
		debug("invalid sign for %s(%s): %s " % (name,sign,callsign))
		sys.exit(1)
	for v_from, v_to in zip(invp, inv):
		if re.match('^[a-zZ]$', v_to):
			mkk = re.match('^(L|F)(\d+)\.(\d+)$',v_from)
			mkp = re.match('^(L|F)(\d+)([a-z])$',v_from)
			if re.match('^[a-zZ]$', v_from): # переменная
				stext = stext + '  mov eax,[ebp+' + str((ord(v_from)-ord('a')+1)*4) + ']' + chr(10) + '  mov [edx+' + str((ord(v_to)-ord('a')+1)*4) + '],eax' + chr(10)
			elif re.match('^Q\d+$', v_from): # мощность комплекса
				stext = stext + '  mov eax,[ebp+' + str((int(v_from[1:])-1)*4+1020) + ']\n  mov [edx+' + str((ord(v_to)-ord('a')+1)*4) + '], eax\n'
			elif re.match('^[a-fA-F0-9]+h$', v_from): # 16-я константа
				stext = stext + '  mov [edx+' + str((ord(v_to)-ord('a')+1)*4) + '],dword ' + v_from + chr(10)
			elif re.match('^\d+$', v_from): # десятичная константа
				stext = stext + '  mov [edx+' + str((ord(v_to)-ord('a')+1)*4) + '],dword ' + v_from + chr(10)
			elif re.match('^\'.\'$', v_from): # символьная константа
				stext = stext + '  mov [edx+' + str((int(v_to)-int('a')+1)*4) + '],dword ' + ord(v_from) + chr(10)
			elif mkk:  # L3.5 F3.5
				nk = int(mkk.group(2))
				stext = stext + '  mov ebx,[ebp+' + str((nk-1)*4+220) + ']\n'
				if mkk.group(1)=='L':
					stext = stext + '  mov eax,[ebx+' + str(int(mkk.group(3))*4) + ']\n'
				else:
					stext = stext + '  mov eax,[ebx+' + mkk.group(3) + ']\n  and eax,0xff\n'
				stext = stext + '  mov [edx+' + str((ord(v_to)-ord('a')+1)*4) + '],eax' + chr(10)
			elif mkp:  # L3h F3h
#				debug(v_from)
#				debug(mkp.group(2))
				nk = int(mkp.group(2))
				stext = stext + '  mov ebx,[ebp+' + str((ord(mkp.group(3))-ord('a')+1)*4) + ']\n'
				if mkp.group(1)=='L':
					stext = stext + '  shl ebx, byte 2\n'
				stext = stext + '  add ebx,[ebp+' + str((nk-1)*4+220) + ']\n  mov eax,[ebx]\n'
				if mkp.group(1)=='F':
					stext = stext + '  and eax,0xff\n'
				stext = stext + '  mov [edx+' + str((ord(v_to)-ord('a')+1)*4) + '],eax' + chr(10)
			else:
				internal_error(stext,'"%s" не является значением переменной' % v_from)
		elif re.match('^(L|F)\d+$',v_to):
			if re.match('^(L|F)\d+$',v_from):
				if v_to[0] == v_from[0]:
					stext = stext + '  mov al,[ebp+' + str(int(v_from[1:])+120) + ']' + chr(10) + '  mov [edx+' + str(int(v_to[1:])+120) + '],al' + chr(10)
					stext = stext + '  mov eax,[ebp+' + str((int(v_from[1:])-1)*4+220) + ']' + chr(10) + '  mov [edx+' + str((int(v_to[1:])-1)*4+220) + '],eax' + chr(10)
					stext = stext + '  mov eax,[ebp+' + str((int(v_from[1:])-1)*4+620) + ']' + chr(10) + '  mov [edx+' + str((int(v_to[1:])-1)*4+620) + '],eax' + chr(10)
					stext = stext + '  mov eax,[ebp+' + str((int(v_from[1:])-1)*4+1020) + ']' + chr(10) + '  mov [edx+' + str((int(v_to[1:])-1)*4+1020) + '],eax' + chr(10)
			else:
				internal_error(stext,'"%s" разные типы комплексов' % v_from)
	for v_from, v_to in zip(outvp, outv):
		if re.match('^(L|F)\d+$',v_to):
			if re.match('^(L|F)\d+$',v_from):
				if v_to[0] == v_from[0]:
					stext = stext + '  mov al,[ebp+' + str(int(v_from[1:])+120) + ']' + chr(10) + '  mov [edx+' + str(int(v_to[1:])+120) + '],al' + chr(10)
					stext = stext + '  mov eax,[ebp+' + str((int(v_from[1:])-1)*4+220) + ']' + chr(10) + '  mov [edx+' + str((int(v_to[1:])-1)*4+220) + '],eax' + chr(10)
					stext = stext + '  mov eax,[ebp+' + str((int(v_from[1:])-1)*4+620) + ']' + chr(10) + '  mov [edx+' + str((int(v_to[1:])-1)*4+620) + '],eax' + chr(10)
					stext = stext + '  mov eax,[ebp+' + str((int(v_from[1:])-1)*4+1020) + ']' + chr(10) + '  mov [edx+' + str((int(v_to[1:])-1)*4+1020) + '],eax' + chr(10)
			else:
				internal_error(stext,'"%s" разные типы комплексов' % v_from)
	stext = stext + '  mov ebp,edx\n  call ' + str(name) + '\n  pop ebp\n  mov edx,esp\n  add esp,1420\n'
	for v_to, v_from in zip(outvp, outv):
		if re.match('^[a-zZ]$', v_from):
			mkk = re.match('^(L|F)(\d+)\.(\d+)$',v_to)
			mkp = re.match('^(L|F)(\d+)([a-z])$',v_to)
			stext = stext + '  mov eax,[edx+' + str((ord(v_from)-ord('a')+1)*4) + ']\n'
			if re.match('^[a-zZ]$', v_to): # переменная
				stext = stext + '  mov [ebp+' + str((ord(v_to)-ord('a')+1)*4) + '],eax\n'
			elif mkk:  # L3.5 F3.5
				nk = int(mkk.group(2))
				stext = stext + '  mov ebx,[ebp+' + str((nk-1)*4+220) + ']\n' 
				if mkk.group(1) == 'F':
					stext = stext + '  mov [ebx+' + mkk.group(3) + '],al\n'
				else:
					stext = stext + '  mov [ebx+' + str(int(mkk.group(3))*4) + '],eax\n'
			elif mkp:  # L3h F3h
#				debug('*****')
#				debug(mkp.group(1))
				nk = int(mkp.group(2))
				stext = stext + '  mov ebx,[ebp+' + str((nk-1)*4+220) + ']\n' 
				stext = stext + '  mov edx,[ebp+' + str((int(m.group(3))-int('a')+1)*4) + ']\n'
				if mkp.group(1) == 'F':
					stext = stext + '  mov [edx+ebx],al\n'
				else:
					stext = stext + '  mov [ebx+edx*4],eax\n'
			else:
				internal_error(stext,'"%s" не является значением переменной' % v_from)
		elif re.match('^(L|F)\d+$',v_to):
			if re.match('^(L|F)\d+$',v_from):
				if v_to[0] == v_from[0]:
					stext = stext + '  mov eax,[edx+' + str((int(v_from[1:])-1)*4+1020) + ']' + chr(10) + '  mov [ebp+' + str((int(v_to[1:])-1)*4+1020) + '],eax' + chr(10)
			else:
				internal_error(stext,'"%s" разные типы комплексов' % v_from)
#	debug(stext)
	return stext

def assign(stext, value, name):
	m = re.match('^[a-z]$', name)
	if m:   # a-z переменные
		stext = stext + '  mov [ebp+' + str((ord(name)-ord('a')+1)*4) + '],' + value + chr(10)
	m = re.match('^Q\d+$', name)
	if m:		# Q1, Q2, Q23
		if (int(name[1:]) > 0) and (int(name[1:]) < 100):
			stext = stext + '  mov [ebp+' + str(int(name[1:])+1020) + '],' + value + chr(10)
	if name == 'Z':
		stext = stext + '  mov [ebp+108],' + value + chr(10)	
	return stext

	
def gettau(stext, name, op):
	m = re.match('^[a-zZ]$', name)
	if m:   # a-z переменные
		stext = stext + '  mov [ebp+' + str(getaddr(name)) + '],eax' + chr(10)
	m = re.match('^I([a-z])$', name)
	if m:	# Ia
		stext = stext + '  ' + op + ' ,[_I+' + str(getaddr(m.group(1))) + ']\n'
	m = re.match('^Q\d+$', name)
	if m:	# Q1, Q2, Q23
		if (int(name[1:]) > 0) and (int(name[1:]) < 100):
			stext = stext + '  mov [ebp+' + str(getaddr(name)) + '],eax' +  chr(10)
	m = re.match('^(L|F)(\d+)\.(\d+)$', name)
	if m:	# L1.0, L5.2, F12.3
		stext = stext + '  mov ebx,[ebp+' + str((int(m.group(2))-1)*4+220) + ']\n'
		if m.group(1) == 'F':
			stext = stext + '  ' + op + ' ' + '[ebx+' + str(int(m.group(3))) + '],al\n'
		else:
			stext = stext + '  ' + op + ' ' + '[ebx+' + str(int(m.group(3))*4) + '],eax\n'
	m = re.match('^(L|F)(\d+)([a-z])$', name)
	if m:	# L1a, L5b, F12c
		stext = stext + '  mov ebx,[ebp+' + str(getaddr(m.group(3))) + ']\n'
		if m.group(1) == 'L':
			stext = stext + '  shl ebx,byte 2\n' 
		stext = stext + '  add ebx,[ebp+' + str((int(m.group(2))-1)*4+220) + ']\n'
		if m.group(1) == 'L':
			stext = stext + '  ' + op + ' [ebx],eax\n'
		else:
			stext = stext + '  ' + op + ' [ebx],al\n'
	return stext

def settau(stext,name,op):
#	debug(name)
	m = re.match('^[a-zZ]$', name)
	if m:   # a-z переменные
		stext = stext + '  ' + op + ' eax,[ebp+' + str(getaddr(name)) + ']' + chr(10)
	m = re.match('^I([a-z])$', name)
	if m:	# Ia
		stext = stext + '  mov ebx,[ebp+'+str(getaddr(m.group(1)))+']\n  and ebx,0x1f\n'
		stext = stext + '  ' + op + ' eax,[_I+ebx*4]\n'
	m = re.match('^I(\d+)$', name)
	if m:	# I8
		stext = stext + '  ' + op + ' eax,[_I+' + str(int(m.group(1))*4) + ']\n'
	m = re.match('^Q\d+$', name)
	if m:		# Q1, Q2, Q23
		stext = stext + '  ' + op + ' eax,[ebp+' + str(getaddr(name)) + ']' + chr(10)
	m = re.match('^(L|F)(\d+)([a-z])$', name)
	if m:	# L1a, L5b, F12c
		stext = stext + '  mov ebx,[ebp+' + str(getaddr(m.group(3))) + ']' + chr(10)
		if m.group(1) == 'L':
			stext = stext + '  shl ebx, byte 2' + chr(10) 
		stext = stext + '  add ebx,[ebp+' + str((int(m.group(2))-1)*4+220) +']\n  '  
		if m.group(1) == 'F':
			stext = stext + 'mov ebx,[ebx]\n  and ebx,0x000000ff\n  ' + op + ' eax,ebx\n'
		else:
			stext = stext +  op + ' eax,[ebx]\n'
	if type(name) == 'int':
		stext = stext + '  ' + op + ' eax,' + str(m.group(2)) +  chr(10)
	m = re.match('^\d+$', name)
	if m:   # десятичная константа
		stext = stext + '  ' + op + ' eax,' + name + chr(10)
	return stext
	
def setreg(stext,name,op,reg):
	m = re.match('^[a-zZ]$', name)
	if m:   # a-z переменные
		stext = stext + '  ' + op + ' ' + reg + ',[ebp+' + str(getaddr(name)) + ']' + chr(10)
	m = re.match('^[Q|S]\d+$', name)
	if m:		# Q1, S2, Q23
		stext = stext + '  ' + op + ' ' + reg + ',[ebp+' + str(getaddr(name)) + ']' + chr(10)
	m = re.match('^(L|F)(\d+)([a-z])$', name)
	if m:	# L1a, L5b, F12c
		stext = stext + '  mov ebx,[ebp+' + str(getaddr(m.group(3))) + ']' + chr(10)
		if m.group(1) == 'L':
			stext = stext + '  shl ebx, byte 2' + chr(10) 
		stext = stext + '  add ebx,[ebp+' + str((int(m.group(2))-1)*4+220) +']\n  '
		if m.group(1) == 'F':
			stext = stext + 'mov ebx,[ebx]\n  and ebx,0x000000ff\n  ' + op + ' ' + reg + ',ebx\n'
		else:
			stext = stext +  op + ' ' + reg +',[ebx]\n'
	m = re.match('^I([a-z])$', name)
	if m:	# Ia
		stext = stext + '  mov ebx,[ebp+' + str(getaddr(m.group(1))) + ']\n  and ebx,0x1f\n'
		stext = stext + '  ' + op + ' ' + reg + ',[_I+ebx*4]\n'
	m = re.match('^I(\d+)$', name)
	if m:	# I8
		stext = stext + '  ' + op + ' ' + reg + ',[_I+'+str(int(m.group(1))*4)+']\n'
	m = re.match('^(L|F)(\d+)\.(\d+)$', name)
	if m:	# L1.0, L5.2, F12.3
		stext = stext + '  mov ebx,[ebp+' + str((int(m.group(2))-1)*4+220) +']\n'
		if m.group(1) == 'F':
			stext = stext + '  ' + op + ' ' + reg + ',[ebx+' + str(int(m.group(3))) +']\n'
			stext = stext + '  and ' + reg + ',0x000000ff\n'
		else:
			stext = stext + '  ' + op + ' ' + reg + ',[ebx+' + str(int(m.group(3))*4) +']\n'
	if type(name) == 'int':
		stext = stext + '  mov ' + reg + ',' + str(m.group(2)) +  chr(10)
	m = re.match('^\d+$', name)
	if m:   # десятичная константа
		stext = stext + '  ' + op + ' ' + reg +',' + name + chr(10)
	m = re.match('^\'.\'$', name)
	if m:	# символьная константа
		stext = stext + '  ' + op + ' ' + reg +',' + str(ord(name[1:2])) + chr(10)
	return stext

def cmpjmp(stext,arg1,cmpop,arg2,mark):
#	debug('cmpop=%s' % cmpop)
	stext = setreg(stext,arg1,'mov','eax')
	stext = stext + '  mov edx,eax' +chr(10)
	stext = setreg(stext,arg2,'mov','eax')
	stext = stext + '  cmp edx,eax' +chr(10)
	op = ''
	if cmpop == '<':
		op = '  jb'
	elif cmpop == '>':
		op = '  ja'
	elif cmpop == '<=':
		op = '  jbe'
	elif cmpop == '>=':
		op = '  jae'
	elif cmpop == '=':
		op = '  je'
	elif cmpop == '#':
		op = '  jne'
	stext = stext + op + ' .P' + mark +chr(10)
	return stext
	
	
def pprog(i, functions, lmas, stext, sdata, mstring):
#	print("name=%s sign=%s code=%s" % (name, sign, code)) 
#	debug("function load signature = '%s', code = '%s'" % (sign, code))
	name = functions[i]
	sign = lmas[name][0]
	code = lmas[name][1]
	mnl = 0
	invars, outvars = re.split('/', sign, 1)
	stext = stext + name + ':' + chr(10)
	while code:
		m = re.match('^\s*\*\*\*.*?\n', code)
		if m:   # комментарий
			code = code[m.end():]
			continue
		m = re.match('^\s*{(.+)}', code)
		if m:	# ассемблерная вставка
			stext = stext + '  ' + m.group(1) + '\n'
			code = code[m.end():]
			continue
#		m = re.match('^\s*(\*\w+)\((\w*\/[a-zZ,\sLF0-9. ]*)\)', code)
		m = re.match('^\s*(\*\w+)\(([a-zZ,\sLFQ0-9. ]*\/[a-zZ,\sLF0-9. ]*)\)', code)
		if m:	# вызов подпрограммы
			lfunc =  m.group(1)[1:]
			stext = call(stext, lfunc, m.group(2), lmas)
			code = code[m.end():]
			ff = 0
			for func in functions:
				if func == lfunc:
					ff = 1
					break
			if ff == 0:
#				debug("func = '%s', lfunc = '%s'" % (func, lfunc))
				functions = functions + [lfunc]
			continue
		m = re.match('^\s*\@\'(.+?)\\\'>(F\d+)', code)
		if m:	# добавление строки к символьному комплексу
			sdata = sdata + '_M' + str(mstring) + ': db ' + '\'' + m.group(1).replace('\\n','\',10,\'') + '\'\n' #_LM'+str(mstring) + ' equ $-_M' + str(mstring) + chr(10)
			ncomp = int(m.group(2)[1:])
			stext = stext + '  add [ebp+' + str((ncomp-1)*4+1020) + '],dword ' + str(len(m.group(1))) + '\n  mov ebx,[ebp+' + str((ncomp-1)*4+620) + ']\n  cmp [ebp+' + str((ncomp-1)*4+1020) + '],ebx\n  ja _errend\n'
			stext = stext + '  mov ecx,' + str(len(m.group(1))) + '\n  mov esi,_M' + str(mstring) + '\n  mov edi,[ebp+' + str((ncomp-1)*4+220) + ']\n  add edi,[ebp+' + str((ncomp-1)*4+1020) + ']\n  sub edi,' + str(len(m.group(1))) + '\n  cld\n  rep movsb\n'
			code = code[m.end():]
			mstring = mstring + 1
			continue
		m = re.match('^\s*/\'(.+?)\\\'>C', code)
		if m:	# вывод строки на экран
			sstring = m.group(1).replace('\\n',chr(10))
			sdata = sdata + '_M' + str(mstring) + ': db \'' + m.group(1).replace('\\n', '\',10,\'')  + '\'\n'
			stext = stext + '  mov eax,4\n  mov ebx,1\n  mov ecx,_M'+ str(mstring) + '\n  mov edx,' + str(len(sstring)) + '\n  int 80h\n'
			code = code[m.end():]
			mstring = mstring + 1
			continue
		m = re.match('^\s*/(F\d+)(<|>)C', code)
		if m:	# ввод/вывод символьного комплекса
			if m.group(2) == '<':
				stext = stext + '  mov eax,3' + chr(10) + '  mov ebx,0' + chr(10)
			else:
				stext = stext + '  mov eax,4' + chr(10) + '  mov ebx,1' + chr(10)
			stext = stext + '  mov ecx,[ebp+'+ str((int(m.group(1)[1:])-1)*4 + 220) + ']' + chr(10)
			if m.group(2) == '<':
				stext = stext + '  mov edx,[ebp+' + str((int(m.group(1)[1:])-1)*4 + 620) + ']' + chr(10)
			else:
				stext = stext + '  mov edx,[ebp+' + str((int(m.group(1)[1:])-1)*4 + 1020) + ']' + chr(10)
			stext = stext + '  int 80h' + chr(10)
			if m.group(2) == '<':
				stext = stext + '  dec eax\n  mov [ebp+' + str((int(m.group(1)[1:])-1)*4 + 1020) + '],eax' + chr(10)
			code = code[m.end():]
#			debug(stext)
#			debug(sdata)
			continue
		m = re.match('^\s*\@\+S(\d+)\((.+?)\)', code)
		if m:	# увеличение ёмкости комплекса 
			stext = appendArray(stext,m.group(1),m.group(2))
			code = code[m.end():]
			continue
		m = re.match('^\s*\@\+((?:L|F)\d+)\((.+?)\)', code)
		if m:	# создание комплекса
			stext = createArray(stext,m.group(1),m.group(2))
			code = code[m.end():]
			continue
		m = re.match('^\s*\@(\-|\%|O)((?:L|F)\d+)', code)
		if m:	# удаление, сокращение, обнуление комплекса
			ncomp = int(m.group(2)[1:])
			if m.group(1) == '-':
				stext = stext + '  mov [ebp+' + str((ncomp-1)*4+220) + '],0\n '
			elif m.group(1) == '%':
				stext = stext + '  mov ebx,[ebp+' + str((ncomp-1)*4+1020) + ']\n   mov [ebp+' + str((ncomp-1)*4+220) + '],ebx\n' 
			else:
				if m.group(2)[0] == L:
					stext = stext + '  xor eax,eax\n'
					oper = '  rep stosd\n'
				else:
					stext = stext + '  xor al,al\n'
					oper = '  rep stosb\n'
				stext = stext + '  mov ecx,[ebp+' + str((ncomp-1)*4+1020) + ']\n  mov edi,[ebp+' + str((ncomp-1)*4+220) + ']\n' + oper
			code = code[m.end():]
			continue
		m = re.match('^\s*\@(\<|\>)((?:L|F)\d+)(?:\.(\d+|[a-z]))?', code)
		if m:	# вставка/извлечение элемента комплекса
			adrnach = (int(m.group(2)[1:])-1)*4+220
			adrmoch = (int(m.group(2)[1:])-1)*4+1020
			nomvstaw = '[ebp+' + str(adrmoch) + ']\n'
			if m.group(3):
				if m.group(3)[0] == '.':
					nomvstaw = m.group(3)[1:] + ']\n'
				else:
					nomvstaw = '[ebp+' + str((ord(m.group(3)[0])-ord('a')+1)*4) + ']\n'
			stext = stext + '  mov ebx,' + nomvstaw
			if m.group(1) == '>':
				if m.group(2)[0] == 'L':
					stext = stext + '  shl ebx,2\n'	# ebx - номер вносимого элемента (eax)
					stext = stext + '  add ebx,[ebp+' + str(adrnach) + ']\n  mov [ebx],eax\n  inc dword [ebp+' + str(adrmoch) + ']\n'
				else:
					stext = stext + '  add ebx,[ebp+' + str(adrnach) + ']\n  mov [ebx],al\n  inc dword [ebp+' + str(adrmoch) + ']\n'
			elif m.group(1) == '<':
				if m.group(2)[0] == 'L':
					stext = stext + '  shl ebx,2\n'	# ebx - номер извлекаемого элемента (eax)
					stext = stext + '  add ebx,[ebp+' + str(adrnach) + ']\n  mov eax,[ebx]\n  dec dword [ebp+' + str(adrmoch) + ']\n'
				else:
					stext = stext + '  add ebx,[ebp+' + str(adrnach) + ']\n  mov al,[ebx]\n  dec dword [ebp+' + str(adrmoch) + ']\n'
			code = code[m.end():]
			continue
		m = re.match('^\s*\@\#L(\d+)L(\d+)\((\d+|[a-z])(?:,\s*(\d+|[a-z])(?:,\s*(\d+|[a-z]))?)?\)', code)
		if m:	# Копирование @#L1L2(h1,h2,h3) :: ecx=h1; esi=A1+h2; edi=A2+h3; if(h3+h1<=S2)  {cld; rep movsb}
			setreg(stext,m.group(3),'mov','ecx');
			stext = stext + '  shl ecx,2\n  mov esi,[ebp+'+ str((int(m.group(1))-1)*4 + 220) + ']' + chr(10)
			if m.group(4) != '':
				setreg(stext,m.group(1),'add','esi');
			stext = stext + '  mov edi,[ebp+'+ str((int(m.group(2))-1)*4 + 220) + ']' + chr(10)
			if m.group(5) == '':
				setreg(stext,'Q'+m.group(2),'add','edi');
			else:
				setreg(stext,m.group(5),'add','edi');
			setreg(stext,'S'+m.group(2),'mov','ebx');			
			stext = stext + '  mov edx,ecx\n  add edx,edi\n  cmp edx,ebx\n  ja _errend\n  cld\n  rep movsb'
			code = code[m.end():]
			continue
#		m = re.match('^\s*\@\#F(\d+)F(\d+)\((\d+|[a-z])(?:,\s*(\d+|[a-z])(?:,\s*(\d+|[a-z]))?)?\)', code)
		m = re.match('^\s*\@\#F(\d+)F(\d+)\((\d+|[a-z])(?:,\s*(\d+|[a-z])(?:,\s*(\d+|[a-z]))?)?\)', code)
		if m:	# Копирование @#F1F2(h1,h2,h3)
#			debug("cmp s1 = '%s', s2 = '%s', s3 = '%s', s4 = '%s', s5 = '%s'" % m.groups())
			setreg(stext,m.group(3),'mov','ecx');
			stext = stext + '  mov esi,[ebp+'+ str((int(m.group(1))-1)*4 + 220) + ']' + chr(10)
			if m.group(4) != '':
				setreg(stext,m.group(1),'add','esi');
			stext = stext + '  mov edi,[ebp+'+ str((int(m.group(2))-1)*4 + 220) + ']' + chr(10)
			if m.group(5):
				debug("s5 = '%s'" % m.group(5))
				setreg(stext,m.group(5),'add','edi');
			else:
				setreg(stext,'Q'+m.group(2),'add','edi');
			setreg(stext,'S'+m.group(2),'mov','ebx');			
			stext = stext + '  mov edx,ecx\n  add edx,edi\n  cmp edx,ebx\n  ja _errend\n  cld\n  rep movsb\n'
			code = code[m.end():]
			continue
		m = re.match('^\s*P(\d+)', code)
		if m:	# параграф	
			stext = stext + '.P' + str(m.group(1)) + ':' + chr(10)
			code = code[m.end():]
			continue
		m = re.match('^\s*\?\=(\d+)', code)
		if m:	# безусловный переход
			stext = stext + '  jmp .P' + str(int(m.group(1))) + chr(10)
			code = code[m.end():]
			continue
		m = re.match('^\s*\?\-(\d+)', code)
		if m:	# переход по нулю
			stext = stext + '  and eax,eax' + chr(10) + '  jz .P' + str(int(m.group(1))) + chr(10)
			code = code[m.end():]
			continue
		m = re.match('^\s*\?\+(\d+)', code)
		if m:	# переход по единице
			stext = stext + '  and eax,eax' + chr(10) + '  jnz .P' + str(int(m.group(1))) + chr(10)
			code = code[m.end():]
			continue
		m = re.match('^\s*\?\((.+?)\s*(\<\=|\>\=|\<|\>|\#|\=)\s*(.+?)\)(\d+)', code)
		if m:	# переход по отношению
#			debug("cmp s1 = '%s', s2 = '%s', s3 = '%s', s4 = '%s'" % m.groups())
			stext = cmpjmp(stext, m.group(1), m.group(2), m.group(3), m.group(4))
			code = code[m.end():]
			continue
		m = re.match('^\s*\?:(\d+)', code)
		if m:	# уход
			stext = stext + '  call .P' + str(int(m.group(1))) + chr(10)
			code = code[m.end():]
			continue
		m = re.match('^\s*\?!', code)
		if m:	# возврат
			stext = stext + '  ret\n'
			code = code[m.end():]
			continue
		m = re.match('^\s*\?X(\d+)([a-z])([a-z])', code)
		if m:	# переход по перебору единиц ?X4ab
#			debug("cmp s1 = '%s', s2 = '%s', s3 = '%s'" % m.groups())
#			mnl=mnl+1
			stext = stext + '  mov eax,[ebp+'+str(getaddr(m.group(2)))+']\n  and eax,eax\n  jz .P'+m.group(1)+'\n  mov edx,eax\n'
			stext = stext + '  dec edx\n  mov esi,eax\n  and esi,edx\n  mov [ebp+'+str(getaddr(m.group(2)))+'],esi\n  xor eax,edx\n'
			stext = stext + '  xor ecx,ecx\n  mov ebx,_vesa\n  xlat\n  add cl,al\n  shr eax,8\n  xlat\n  add cl,al\n  shr eax,8\n  xlat\n  add cl,al\n  shr eax,8\n  xlat\n  add cl,al\n  mov eax,ecx\n'
			stext = stext + '  dec ecx\n  mov [ebp+'+str(getaddr(m.group(3)))+'],ecx\n'
			code = code[m.end():]
			continue
		m = re.match('^\s*(\+|\-|\*|\||\&|\#|\<|\>|\:|\/|\;|)\s*((?:[a-fA-F0-9]+h)|(?:[01]+b)|(?:0[0-7]+)|(?:\d+)|(?:\'.\'))', code)
		if m:	# operators с константами
			if m.group(2)[-1] == 'b':
				tmp = int(m.group(2)[:-1], 2)
			elif m.group(2)[-1] == 'h':
				tmp = int(m.group(2)[:-1], 16)
			elif m.group(2)[0] == '0':
				tmp = int(m.group(2), 8)
			elif m.group(2)[0] == '\'':
				tmp = ord(m.group(2)[1:2])
			else:
				tmp = int(m.group(2), 10)
			if m.group(1) == '': 	# constanta
				stext = settau(stext,str(tmp),'mov')
			elif m.group(1) == '+' : # add
				stext = stext + '  add eax,' + str(tmp) + chr(10)
			elif m.group(1) == '-' : #sub',
				stext = stext + '  sub eax,' + str(tmp) + chr(10)
			elif m.group(1) == '*' : #mul',
				stext = stext + '  mov edx,' + str(tmp) + '\n  mul edx\n  mov [ebp+108],edx\n'
			elif m.group(1) == '|' : #or',
				stext = stext + '  or eax,' + str(tmp) + chr(10)
			elif m.group(1) == '&' : #and',
				stext = stext + '  and eax,' + str(tmp) + chr(10)
			elif m.group(1) == '#' : #xor',
				stext = stext + '  xor eax,' + str(tmp) + chr(10)
			elif m.group(1) == '<' : #shiftleft',       
				stext = stext + '  shl eax, byte ' + str(tmp) + chr(10)
			elif m.group(1) == '>' : #shiftright',
				stext = stext + '  shr eax, byte ' + str(tmp) + chr(10)
			elif m.group(1) == ':' : #divdouble',
				stext = stext + '  mov ebx,' + str(tmp) + '\n  mov edx,[ebp+108]\n  div ebx\n'
			elif m.group(1) == '/' : #divmod',
				stext = stext + '  mov ebx,' + str(tmp) + '\n  xor edx,edx\n  div ebx\n  mov [ebp+108],edx\n'
			elif m.group(1) == ';' : #moddiv'
				stext = stext + '  mov ebx,' + str(tmp) + '\n  xor edx,edx\n  div ebx\n  mov [ebp+108],eax\n  mov eax,edx\n'
			code = code[m.end():]
			continue
		m = re.match('^\s*(\=|O|D|Y|\_|\+|\-|\*|\||\&|\#|\<|\>|\:|\/|\;|)\s*([a-zZ]|(?:I\d+)|(?:I[a-z])|(?:Q\d+)|(?:(?:L|F)(?:(?:(?:\d+)[a-zZ])|(?:[a-zZ](?:\d+))))|(?:(?:L|F)(?:\d+).(?:\d+))|(?:(?:Q|S)(?:(?:\d+)|[a-zZ])))', code)
		if m :	# операция с переменной
			if m.group(1) == '': 		# var
#				debug(m.group(2))
				stext = setreg(stext,m.group(2),'mov','eax')
			elif m.group(1) == '=': 	# assign
				stext = gettau(stext,m.group(2),'mov')
			elif m.group(1) == 'D' : 	# increment
				stext = settau(stext,m.group(2),'mov')
				stext = stext + '  inc eax' + chr(10)
				stext = gettau(stext,m.group(2),'mov')
			elif m.group(1) == 'Y': 	# decrement
				stext = settau(stext,m.group(2),'mov')
				stext = stext + '  dec eax' + chr(10)
				stext = gettau(stext,m.group(2),'mov')
			elif m.group(1) ==	'O' : 	# null
				stext = stext + '  xor eax,eax' + chr(10)
				stext = gettau(stext,m.group(2),'mov')
			elif m.group(1) ==	'_' : 	# max
				stext = stext + '  mov eax,0xffffffff' + chr(10)
				stext = gettau(stext,m.group(2),'mov')
			elif m.group(1) ==	'+' : 	# addvar
				stext = setreg(stext,m.group(2),'add','eax')
			elif m.group(1) ==	'-' : 	# subvar
				stext = setreg(stext,m.group(2),'sub','eax')
			elif m.group(1) ==	'*' : 	# mulvar
				stext = setreg(stext,m.group(2),'mov','ebx')
				stext = stext + '  mul ebx\n  mov [ebp+108],edx\n'
			elif m.group(1) ==	'|' : 	# orvar
				stext = setreg(stext,m.group(2),'or','eax')
			elif m.group(1) ==	'&' : 	# andvar
				stext = setreg(stext,m.group(2),'and','eax')
			elif m.group(1) ==	'#' : 	# xorvar
#				debug(m.group(2))
				stext = setreg(stext,m.group(2),'xor','eax')
			elif m.group(1) ==	'<' : 	# shiftleftvar
				stext = setreg(stext,m.group(2),'mov','cl')
				stext = stext + '  shl eax,cl\n'
			elif m.group(1) == '>' : 	# shiftrightvar
				stext = setreg(stext,m.group(2),'mov','cl')
				stext = stext + '  shr eax,cl\n'
			elif m.group(1) == ':' : 	# divdoublevar
				stext = stext + '  mov edx,[ebp+108]\n'
				stext = setreg(stext,m.group(2),'mov','ebx')
				stext = stext + '  div ebx\n'
			elif m.group(1) == '/' : 	# divmodvar
				stext = stext + '  xor edx,edx\n'
				stext = setreg(stext,m.group(2),'mov','ebx')
				stext = stext + '  div ebx\n  mov [ebp+108],edx\n'
			elif m.group(1) == ';' : 	# moddivvar
				stext = stext + '  xor edx,edx\n'
				stext = setreg(stext,m.group(2),'mov','ebx')
				stext = stext + '  div ebx\n  push eax\n  push edx\n  pop eax\n  pop dword[ebp+108]\n'
			code = code[m.end():]
			continue
        # operations
		m = re.match('^\s*X', code)
		if m:		# random generation
			stext = stext + '  mov eax,[_rand]\n  mov edx,97781173\n  mul edx\n  add eax,800001\n  mov [_rand],eax\n'
			code = code[m.end():]
			continue
		m = re.match('^\s*T', code)
		if m:		# time
			stext = stext + '  mov eax,13\n  mov ebx,0\n  int 80h\n'
			code = code[m.end():]
			continue
		m = re.match('^\s*%', code)
		if m:		# weight
			stext = stext + '  xor ecx,ecx\n  mov ebx,_vesa\n  xlat\n  add cl,al\n  shr eax,8\n  xlat\n  add cl,al\n  shr eax,8\n  xlat\n  add cl,al\n  shr eax,8\n  xlat\n  add cl,al\n  mov eax,ecx\n'
			code = code[m.end():]
			continue
		m = re.match('^\s*~', code)
		if m:		# inverse
			stext = stext + '  not eax\n'
			code = code[m.end():]
			continue
		m = re.match('^\s*\!', code)
		if m:		# number of little one
			stext = stext + '  mov ebx,eax\n  dec eax\n  xor eax,ebx\n'
			stext = stext + '  xor ecx,ecx\n  mov ebx,_vesa\n  xlat\n  add cl,al\n  shr eax,8\n  xlat\n  add cl,al\n  shr eax,8\n  xlat\n  add cl,al\n  shr eax,8\n  xlat\n  add cl,al\n  dec cl\n  mov eax,ecx\n'
			code = code[m.end():]
			continue
		m = re.match('^\s*=\(([a-zZ])([a-zZ])\)', code)
		if m:		# =(ab)
			stext = stext + '  mov esi,[ebp+' + str((ord(m.group(1))-ord('a')+1)*4) + ']\n  mov edi,[ebp+' + str((ord(m.group(2))-ord('a')+1)*4) + ']\n'
			stext = stext + '  push dword [esi]\n  push dword [edi]\n  pop dword [edi]\n  pop dword [esi]\n'
			code = code[m.end():]
			continue
		m = re.match('^\s*=\(((?:L|F)\d+)([a-zZ])([a-zZ])\)', code)
		if m:	# обмен элементов комплекса =(L1ab)
			nachkom = str((int(m.group(1)[1:])-1)* 4+220)
			if m.group(1)[0] == 'F':
				stext = stext + '  mov esi,[ebp+' + str((ord(m.group(2))-ord('a')+1)*4) + ']\n  add esi,[ebp+' + nachkom + ']\n  mov edi,[ebp+' + str((ord(m.group(3))-ord('a')+1)*4) + ']\n  add edi,[ebp+' + nachkom + ']\n'
				stext = stext + '  mov al,[esi]\n  mov bl,[edi]\n  mov [esi],bl\n  mov [edi],al\n'
			else:
				stext = stext + '  mov ebx,[ebp+' + str((ord(m.group(2))-ord('a')+1)*4) + ']\n  mov edx,[ebp+'+ nachkom + ']\n  lea esi,[edx+ebx*4]\n  mov ebx,[ebp+' + str((ord(m.group(3))-ord('a')+1)*4) + ']\n  mov edx,[ebp+' + nachkom + ']\n  lea edi,[edx+ebx*4]\n'
				stext = stext + '  push dword [esi]\n  push dword [edi]\n  pop dword [esi]\n  pop dword [edi]\n'
			code = code[m.end():]
			continue
		m = re.match('^\s*=\(((?:L|F)\d+)([a-zZ])(\d+)\)', code)
		if m:		# обмен элементов комплекса =(L1a25)
			nachkom = str((int(m.group(1)[1:])-1)* 4+220)
			if m.group(1)[0] == 'F':
				stext = stext + '  mov esi,[ebp+' + str((ord(m.group(2))-ord('a')+1)*4) + ']\n  add esi,[ebp+' + nachkom + ']\n  mov edi,[ebp+' + nachkom + int(m.group(3))+']\n'
				stext = stext + '  mov al,[esi]\n  mov bl,[edi]\n  mov [esi],bl\n  mov [edi],al\n'
			else:
				stext = stext + '  mov esi,[ebp+' + str((ord(m.group(2))-ord('a')+1)*4) + ']\n  add esi,[ebp+' + nachkom + ']\n  mov edi,[ebp+' + nachkom + int(m.group(3))+']\n'
				stext = stext + '  push dword [esi]\n  push dword [edi]\n  pop dword [esi]\n  pop dword [edi]\n'
			code = code[m.end():]
			continue
		m = re.match('^\s*=\(((?:L|F)\d+)\.(\d+)([a-zZ])\)', code)
		if m:		# обмен элементов комплекса =(L1.25a)
			nachkom = str((int(m.group(1)[1:])-1)* 4+220)
			if m.group(1)[0] == 'F':
				stext = stext + '  mov esi,[ebp+' + int(m.group(2)) + nachkom + ']\n  mov edi,[ebp+' + str((ord(m.group(3))-ord('a')+1)*4) + ']\n  add edi,[ebp+' + nachkom + ']\n'
				stext = stext + '  mov al,[esi]\n  mov bl,[edi]\n  mov [esi],bl\n  mov [edi],al\n'
			else:
				stext = stext + '  mov esi,[ebp+' + int(m.group(2)) + ']+' + nachkom + ']\n  mov edi,[ebp+' + str((ord(m.group(3))-ord('a')+1)*4) + ']\n  add edi,[ebp+' + nachkom + ']\n'
				stext = stext + '  push dword [esi]\n  push dword [edi]\n  pop dword [esi]\n  pop dword [edi]\n'
			code = code[m.end():]
			continue
		m = re.match('^\s*\*\*', code)
		if m:       # конец программы
			break
		print("tail of code = '"+code+"'\nUnknown construction. quit\n\n")
		code = ''
#		internal_error(stext,"tail of code = '"+code+"' Unknown construction. quit")
	stext = stext + '  ret' + chr(10)
#	debug('code after compile %s' % chr(10)+stext)
	return functions,stext,sdata,mstring

def load(source,lteka):
#    debug("load code = '%s'" % (source))
	lmas = {}
	scode = re.split('(?:\n|^)([a-zA-Z0-9_]+)\(([a-zA-Z0-9,\s/]+)\)', source)[1:]
#	scode = re.split('(?:\n\s*|^\s*)([a-zA-Z0-9_]+)\(([a-zA-Z0-9,\s/]+)\)', source)[1:]
	functions = [scode[0]]
#	debug("startname = '%s'" % startname)
	scode = re.split('(?:\n|^)([a-zA-Z0-9_]+)\(([a-zA-Z0-9,\s/]+)\)', lteka)[1:]
	while scode:
		name, sign, body, scode = scode[0], scode[1], scode[2], scode[3:]
		lmas[name] = (sign, body)
	scode = re.split('(?:\n|^)([a-zA-Z0-9_]+)\(([a-zA-Z0-9,\s/]+)\)', source)[1:]
	while scode:
		name, sign, body, scode = scode[0], scode[1], scode[2], scode[3:]
		lmas[name] = (sign, body)
	sdata = 'section .data\n_sizebim dd 0\n_addrbim dd 0\n_rand dd 0xa1248aa9\n\
_vesa: \n\
  db 0,1,1,2,1,2,2,3,1,2,2,3,2,3,3,4\n\
  db 1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5\n\
  db 1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5\n\
  db 2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6\n\
  db 1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5\n\
  db 2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6\n\
  db 2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6\n\
  db 3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7\n\
  db 1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5\n\
  db 2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6\n\
  db 2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6\n\
  db 3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7\n\
  db 2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6\n\
  db 3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7\n\
  db 3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7\n\
  db 4,5,5,6,5,6,6,7,5,6,6,7,6,7,7,8'
	sdata = sdata + '\n\
_I: \n\
  dd 0x1,0x2,0x4,0x8,0x10,0x20,0x40,0x80,0x100,0x200,0x400,0x800,0x1000,0x2000,0x4000,0x8000\n\
  dd 0x10000,0x20000,0x40000,0x80000,0x100000,0x200000,0x400000,0x800000\n\
  dd 0x1000000,0x2000000,0x4000000,0x8000000,0x10000000,0x20000000,0x40000000,0x80000000\n' 
	stext = 'global _start\nsection .text\n_start:\n  mov eax,45\n  xor ebx,ebx\n  int 80h\n\
	mov [_sizebim],eax\n  mov [_addrbim],eax\n  sub esp,1420\n  push ebp\n  mov  ebp,esp\n' 
	stext = stext + '  call ' + functions[0] + '\n  mov eax,1\n  mov ebx,0\n  int 80h\n' 
	i = 0
	mstring = 1
	while i < len(functions):
		functions,stext,sdata,mstring = pprog(i, functions, lmas, stext, sdata, mstring)
		i = i+1
		if mstring == 0:
			break
	stext.replace('\\n',chr(10))
	sdata.replace('\\n',chr(10))
	bibl = '_addmem:\n  push eax\n  push ebx\n  mov ebx,[_addrbim]\n  cmp ebx,[_sizebim]\n\
  jbe .end\n  sub ebx,[_sizebim]\n  add ebx,1000h\n  add ebx,[_sizebim]\n  mov eax,45\n  int 80h\n\
  and eax,eax\n  jnz ._errend\n  mov eax,1\n  mov ebx,1\n  int 80h\n._errend:\n  mov [_sizebim],ebx\n.end:\n  pop ebx\n  pop eax\n  ret\n\
_errend:\n  mov eax,1\n  mov ebx,1\n  int 80h\n'
	bibl.replace('\\n', chr(10))
	#print('%s' % sdata)
	#print('%s' % stext)
	#print('%s' % bibl)
	return stext+bibl+sdata, mstring
 
def loadfile(filename):
    fd = open(filename, 'r');
    code = ''.join(fd.readlines())
    fd.close()
    return code

if __name__ == "__main__":
	code = loadfile(sys.argv[1])
	lteka = loadfile("./libl0.l")
	stext,f = load(code,lteka)
	m = re.match('(\w+)', sys.argv[1])    	
	sfile = str(m.group(1))
#	debug(sfile)
	fd = open(sfile+'.s', 'w')
	fd.write(stext)
	fd.close()
	if f > 0:
		cname = 'nasm -felf -g '+sfile+'.s'
		os.system(cname)
		cname = 'ld -melf_i386 -o '+sfile+' '+sfile+'.o'
		os.system(cname)
		os.remove(sfile+'.o')
		print('compilation done, '+sfile)
#run program
 
