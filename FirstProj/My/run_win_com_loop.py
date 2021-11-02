'''
Created on 25 окт. 2021 г.

@author: iamclock
'''
# -*- coding: utf-8 -*-
import os
from subprocess import Popen, PIPE 
from string import ascii_lowercase, digits
from random import choice, seed
from inspect import stack
import logging
import re


logFile = "container.log"
logging.basicConfig(level=logging.INFO, filename=logFile, format='%(asctime)s %(levelname)s:%(message)s')
containers = []
templateSymbols = ascii_lowercase + digits
suffixes = [
    # "1",
    # "2",
    "3",
    "4"
    ]
options = dict(zip(suffixes, [
    # "\"1\"",
    # "\"2\"",
    "\"3\"",
    "\"4\""
    ]))
keysCount = 1000

def whoami():
    return stack()[1][3]

def lfsr(register, polynom):
    '''
    регистр сдвига с линейной обратной связью
    register - текущее состояние регистра
    polynom - примитивный многочлен
    '''
    bit = register & 1
    register >>= 1
    if bit:
        register = register ^ polynom
    return register, bit

def enum():
    comm = f"\"enum"
    output, _ = execute(comm)
    return output

def genKey(containerName, opts, is_print=False):
    '''
    Генерация ключа
    '''
    comm = f"\"gen --name {containerName} --alg {opts} --name {containerName}"
    output, _ = execute(comm)
    if is_print:
        print("\n", comm)
        print(output, "\n")
    assert re.search(r".*Success.*", output), f"[{whoami()}] {comm} : Not success : {output}."
    return output

def rmContainer(containerName, is_print=False):
    comm = f"\"del -n {containerName}"
    output, _ = execute(comm)
    if is_print:
        print("\n", comm)
        print(output, "\n")
    assert re.search(r".*Success.*", output), f"[{whoami()}] {comm} : Not success : {output}."
    return output

def checkKey(keysList, containerName):
    '''
    Проверка, что ключ сгенерировался, контейнер создался
    '''
    assert containerName in keysList, f"[{whoami()}] : container {containerName} is not in the list"
    logging.debug(f"[{whoami()}] : container {containerName} is in the list")
    # print("checkKey: Passed")
    return

def execute(command):
    res = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    output = res.stdout.read() # .decode('utf-8').strip()
    output += res.stderr.read() #.decode('utf-8').strip()
    output = output.decode('utf-8').strip()
    return output, res.returncode

def genAllKeys(containerName):
    '''
    Генерация ключей
    '''
    for suffix in suffixes:
        curContName = f"{containerName}{suffix}"
        try:
            _ = genKey(curContName, options[suffix], is_print=False)
        except AssertionError as er:
            logging.error(er)
            print("[ERROR]", er)
    return

def checkAllKeys(containerName):
    '''
    Проверка, что все ключи сгенерировались, контейнеры создались
    '''
    keysList = enum()
    for suffix in suffixes:
        curContName = f"{containerName}{suffix}"
        try:
            checkKey(keysList, curContName)
        except AssertionError as er:
            logging.error(f"{er}")
            print("[ERROR]", er)
            printEnum()
    # print("checkKey: Passed")
    return

def printEnum():
    output = enum()
    print(output)
    # if 'Success' in output:
    #     print("enum: Passed")
    return

def removeContainers():
    '''
    Удаление контейнеров
    '''
    while True:
        try:
            curContainerPrefix = containers.pop()
        except IndexError:
            logging.info(f"[{whoami()}]\t: No containers remaining")
            break
        for suffix in suffixes:
            curContainerName = f"{curContainerPrefix}{suffix}"
            try:
                _ = rmContainer(curContainerName, is_print=False)
            except AssertionError as er:
                logging.error(er)
                print("[ERROR]", er)
    return


if __name__ == '__main__':
#     path = ""
#     os.chdir(path)
    j = 0
    while True:
        # rho3fe28r0r : 0xe8
        # kyxmpced1as : 0xf2d
        # 6Yp2f3uoslh : 0xb43
        lfsrSeed = 0x1
        lfsrMask = 0xb43
        lfsrCurState, _ = lfsr(lfsrSeed, lfsrMask)
        j += 1
        startCleanUpCount = 200 # требуемое количество контейнеров для запуска очистки 
    #     i = 0
    #     while lfsrSeed != lfsrCurState:
    #         i += 1
        # lfsrErrorSeedList = [0xb43]
        # for lfsrCurState in lfsrErrorSeedList:
        for i in range(0, keysCount):
            seed(lfsrCurState)
            newContainer = (''.join(choice(templateSymbols) for _ in range(11)))
            containers.append(newContainer)
            genAllKeys(newContainer)
            checkAllKeys(newContainer)
            lfsrCurState, _ = lfsr(lfsrCurState, lfsrMask)
            if not ((i + 1) % startCleanUpCount): # очистка списка созданных токенов каждые n раз
                removeContainers()
        logMsg = f"Iteration: {j}, Keys count: {(i+1)*2}"
        logging.info(logMsg)
        print(logMsg)
        # break # for debuging purposes