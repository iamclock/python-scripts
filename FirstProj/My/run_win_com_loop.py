'''
Created on 10 окт. 2021 г.

@author: iamclock
'''
# -*- coding: utf-8 -*-
import os
from subprocess import Popen, PIPE 
from string import ascii_letters, digits
from random import choice, seed

containers = []
templateSymbols = ascii_letters + digits

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

def execute(command):
    res = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    output = res.stdout.read().decode('utf-8')
    output += res.stderr.read().decode('utf-8')
    return output, res.returncode

def genKey(containerName):
    suffixes = ["_256", "_512"]
    options = dict(zip(suffixes, [["", ""]]))
    for suffix in suffixes:
        curContName = f"{containerName}{suffix}"
        comm = f" {curContName} {options[suffix]} {curContName} "
        print(comm)
        # output, retCode = execute(comm)
        # if retCode > 0:
        #     print(output)
        #     raise ValueError("genKey suffix[1:] key: Return code doesn't equals 0")
    return

def checkKey(containerName):
    suffixes = ["_256", "_512"]
    comm = f""
    output, retCode = execute(comm)
    if retCode == 0:
        for suffix in suffixes:
            curContName = f"{containerName}{suffix}"
            if not curContName in output:
                raise ValueError(f"checkKey: container {curContName} is not in the list")
            else:
#                 print(f"checkKey: container {curContainerName} is in the list")
                pass
    else:
        print(output)
        raise ValueError("checkKey: Return code doesn't equals 0")
    return

def enum():
    return

def remContainers():
    suffixes = ["_256", "_512"]
    while True:
        try:
            curContainerPrefix = containers.pop()
        except IndexError:
            print("remContainers: No containers remaining")
            break
        for suffix in suffixes:
            curContainerName = f"{curContainerPrefix}{suffix}"
#             comm = f" {curContainerName}"
#             execute(comm)
#             print(f"remContainers: container {curContainerName} successfully deleted")
    return


if __name__ == '__main__':
#     path = "C:\Users\User"
#     os.chdir(path)
    j = 0
    while True:
        lfsrSeed = 0x1
        lfsrMask = 0xb43
        lfsrCurState, _ = lfsr(lfsrSeed, lfsrMask)
        j += 1
    #     i = 0
    #     while lfsrSeed != lfsrCurState:
    #         i += 1
        for i in range(0, 501):
            seed(lfsrCurState)
            newContainer = (''.join(choice(templateSymbols) for _ in range(10)))
            containers.append(newContainer)
            """
            try:
                genKey(newContainer)
                checkKey(newContainer)
            except ValueError:
                print("Wrong return code")
                return
            """
    #         print(i, hex(lfsrCurState), sep='\t')
            lfsrCurState, _ = lfsr(lfsrCurState, lfsrMask)
#         print("        Containers:", )
#         print(*containers, sep='\n', end="\n")
#         print("        Remove containers:")
        remContainers()
#         print("        Containers:")
#         print(*containers, sep='\n', end="\n")
        print(j, i, sep="\t")
#         break
#     return