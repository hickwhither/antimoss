import sys
import os

import random
import string

import time


# file = sys.argv[1]


strs = string.ascii_letters + string.digits
def randomstr() -> str:
    return random.choice(string.ascii_letters) + ''.join(random.choices(strs, k=random.randint(11, 25)))
def randomnum() -> str:
    return f'({random.randint(int(-1e8), int(1e8))})'

# +00 for random operate
# ;;; for random command
# /// for random define

# ### for random string
# $$$ for random number

rdcommand = [
'''while
(false){for(;false;){}
cout << "###";
for(;false;){}
}''',

'''for(;false;)
{for(;false;)if(false){};
cout << "###";cout << $$$;for(;false;){
}}''',

'''do{break;
cout << +00;{{cout
<<"###";}}
}
while(true);''',
]

rddefine = [
'#define ### ###',

'''void ###(int sos)
{
    cout << "###";;;
    return;;;
}''',

'''
int ###(int a, int ###){
        cout << 0 +00 +00;;;
cout << "###";;;
            return a++00+00;;;
}
''',

'''
bool ###(int ###, string ###){
    cout<<$$$;
    ;;; ;;; ;;;
    ;;; cout<< 00 +00;;;
    return 0;;;
}
''',

'''
string ###(const int &x){
if(x==0)return "###";;;
    return "###";;;
}
''',

'''
#define ###(conc) conc+$$$
''',

'''
#define ###(a, b) a-1+b+00^a+00^b+b
'''

'''
struct ###{
    int ###;
    void ###(){
        cout << 1+00;;;
        cout << 1^2+00;;;
    }
};
'''

]

rdoperate = [
'+min(0,0+1)',
'+max(0,0-1)',
'+abs($$$)*$$$*0',
'+int(bool(0))',
'+$$$*0',
'+$$$-$$$',
'-$$$+$$$',
'^($$$^$$$)',
'max(min($$$,0),0)',
'max(min(0,$$$),0)',
'min(max($$$,0),0)',
'min(max(0,$$$),0)',
'(0==1 ? $$$ : 0)',
'(true ? 0 : $$$)',
'(bool($$$) ? 0 : $$$*$$$)',
]

def antimoss(code):
    while code.find('///') != -1:
        s = random.choice(rddefine)
        while s.find('$$$') != -1: s = s.replace('$$$', randomnum(), 1)
        while s.find('###') != -1: s = s.replace('###', randomstr(), 1)
        code = code.replace('///', s, 1)

    while code.find(';;;') != -1:
        s = ';'+random.choice(rdcommand)
        while s.find('$$$') != -1: s = s.replace('$$$', randomnum(), 1)
        while s.find('###') != -1: s = s.replace('###', randomstr(), 1)
        code = code.replace(';;;', s, 1)

    while code.find('+00') != -1:
        s = random.choice(rdoperate)
        while s.find('$$$') != -1: s = s.replace('$$$', randomnum())
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

