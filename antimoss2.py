import sys
import os

import random
import string

import time



STR = string.ascii_letters + string.digits + '_'
def randomstr() -> str: 
    return random.choice(string.ascii_letters+'_') + ''.join(random.choices(STR, k=random.randint(12, 25)))
def randomnum() -> str:
    return f'({random.randint(int(-1e8), int(1e8))})'

# +00 for random =0
# ;;; for random command
# /// for random function delclare

# for single:
# ??? random types
# ### random string
# $$$ random number

types = [
'bool', 'string',
'float', 'double', 'long double',
'char', 'unsigned char', 'signed char',
'int', 'unsigned int', 'signed int',
'short', 'unsigned short', 'signed short',
'long long', 'unsigned long long', 'signed long long',
'uint16_t', 'uint32_t', 'uint64_t', 'uint8_t',
'uint_fast16_t', 'uint_fast32_t', 'uint_fast64_t', 'uint_fast8_t',
'uint_least16_t', 'uint_least32_t', 'uint_least64_t', 'uint_least8_t',
'int16_t', 'int32_t', 'int64_t', 'int8_t',
'int_fast16_t', 'int_fast32_t', 'int_fast64_t', 'int_fast8_t',
'int_least16_t', 'int_least32_t', 'int_least64_t', 'int_least8_t',
]


bracketinsiders = [
'while ( +00 ) { ;;; }',
'do {break; {} ;;; } while( +00 )',
'for ( ;+00; +00) { ;;; }',
]
singlecommands = [
'cout << +00;',
'cout << "###";',
'cerr << +00;',
'cerr << "###";',
'"###";',
'+00;',
]
equalsrandom = [
' +01 + +01 ',
' +01 - +01 ',
' +01 * +01 ',
' +01 % +01 ',
'min (+01,+01)',
'max (+01,+01)',
'min (+01,+01)',
'__builtin_popcount ( +01 ) ',
'__builtin_parity ( +01 )',
'__builtin_clz ( +01 ) ',
'__builtin_ctz ( +01 )',
'cos ( +01 )',
'sin ( +01 )',
'tan ( +01 )',
'acos ( +01 ) ',
'acos ( +01 ) ',
'asin ( +01 ) ',
'atan ( +01 ) ',
'cosh ( +01 ) ',
'sinh ( +01 ) ',
'tanh ( +01 ) ',
'acosh ( +01 ) ',
'asinh ( +01 ) ',
'atanh ( +01 ) ',
'exp ( +01 ) ',
'log ( +01 ) ',
'log10 ( +01 ) ',
'exp2 ( +01 ) ',
'expm1 ( +01 ) ',
'ilogb ( +01 ) ',
'log1p ( +01 ) ',
'log2 ( +01 ) ',
'logb ( +01 ) ',
'sqrt ( +01 ) ',
'cbrt ( +01 ) ',
'ceil ( +01 ) ',
'floor ( +01 ) ',
'fmod ( +01 , +01 ) ',
'trunc ( +01 ) ',
'round ( +01 ) ',
'lround ( +01 ) ',
'llround ( +01 ) ',
'rint ( +01 ) ',
'lrint ( +01 ) ',
'llrint ( +01 ) ',
'nearbyint ( +01 ) ',
'abs ( +01 ) ',
'atan2 ( +01 , +01 ) ',
'pow ( +01, +01 ) ',
'isfinite ( +01 ) ',
'isinf ( +01 ) ',
'isnan ( +01 ) ',
'isnormal ( +01 ) ',
'signbit ( +01 ) ',
]

# globalvar = []
# globalfunc = []


def equalrandom(depth=0):
    if depth>4: return randomnum()
    if random.randint(0,1)==0: return randomnum()
    s = random.choice(equalsrandom)
    while s.find('+01') != -1:
        s = s.replace('+01', equalrandom(depth+1), 1)
    s = f'int ( {s} ) '
    while s.find(' ') != -1:
        s = s.replace(' ', random.choice(['\n', '']), 1)
    return f'int({s})'

def equalzero(): return f'{equalrandom()}*0'

def singlecommand():
    s = random.choice(singlecommands)
    while s.find('+00') != -1:
        s = s.replace('+00', equalzero(), 1)
    while s.find('$$$') != -1:
        s = s.replace('$$$', randomnum(), 1)
    while s.find('###') != -1:
        s = s.replace('###', randomstr(), 1)
    return s


def complicatedcommand(depth=0):
    s = random.choice(bracketinsiders)
    s = bracketinsiders[1]
    while s.find(' ') != -1:
        s = s.replace(' ', random.choice(['\n', '']), 1)
    while s.find('+00') != -1:
        s = s.replace('+00', f'{equalrandom()}*0', 1)
    t = random.randint(0, 100)
    if depth>2 or t<80: c = singlecommand()
    elif t<95: c = complicatedcommand(depth+1)
    elif t<97: c = '\n'.join(complicatedcommand(depth+1) for i in range(2))
    else: c = '\n'.join(complicatedcommand(depth+1) for i in range(3))
    s = s.replace(';;;', c)
    return s + ';'


def randomdefine():
    return f"#define {randomstr()} {randomstr()}"

def singledeclare():
    return f"{random.choice(types)} {randomstr()}"
def multideclare(r=None):
    r = r or random.randint(1,5)
    return f"{random.choice(types)} {','.join(randomstr() for i in range(r))}" + ';'
def infuncdeclare(r=None):
    r = r or random.randint(1,5)
    return f"{random.choice(['\n', ''])},{random.choice(['\n', ''])}".join(f"{random.choice(types)} {randomstr()}" for i in range(r))


def randomfunc():
    name = randomstr()
    args_size = random.randint(0, 5)
    # call_func = f'{name} ( {' , '.join(equalzero() for i in range(args_size))} ) '
    # globalfunc.append((name, args_size))
    s = f'{random.choice(types)} {name}({infuncdeclare(args_size)})\u007b {complicatedcommand()} \u007d'
    return s


def antimoss(code):
    while code.find('///') != -1:
        t = random.randint(0, 3)
        if t==0: s = randomdefine()
        elif t==1: s = multideclare()
        else: s=randomfunc()
        code = code.replace('///', s, 1)

    while code.find(';;;') != -1:
        s = ';' + complicatedcommand()
        code = code.replace(';;;', s, 1)

    while code.find('+00') != -1:
        s = equalzero()
        code = code.replace('+00', s, 1)
    
    return code


if __name__ == '__main__':
    file = sys.argv[1]
    name, extend = os.path.splitext(file)
    file2 = f'{name}_result{extend}' if(len(sys.argv)<3) else sys.argv[2]

    with open(file, 'r') as f:
        code = f.read()

    code = antimoss(code)

    with open(file2, 'w') as f:
        f.write(code)

