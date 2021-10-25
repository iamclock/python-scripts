#! /usr/bin/env python3




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


def chk_period():
    #seed = reg = 0x3fffffff
    #poly = 0x200004E1
    #seed = reg = 0xace1
    #poly = 0xb400
    #seed = reg = 0xaffffffff
    #poly = 0x4000006E3
    #seed = reg = 0xffffffff
    #poly = 0x80000A92
    seed = reg = 0x1
    poly = 0x5
    
    period = 0
    print(str(hex(reg)))
    while True:
        reg, bit = lfsr(reg, poly)
        print(bit, end="")
        #print(str(hex(reg)))
        period += 1
        if reg == seed:
            break
    print()
    print(str(hex(reg)))
    print(str(period))


#def main():
chk_period()

