def di_gui(n):
    print(n, "<===1====>")
    if n > 0:
        di_gui(n - 1)
    print(n, '<===2====>')
di_gui(3)

import sys
res=sys.getrecursionlimit()
print(res)

def jie_cheng(n):
    print('一次过程')
    if n <= 1:
        return 1
    return n * jie_cheng(n - 1)

res = jie_cheng(5)    
print(res)


a = 190.0
int(a)

print(a)
