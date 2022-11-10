'''
Author : Decheng Fang
Email: fangdecheng@hotmail.com
Github: https://github.com/fdc227
Liscense: MIT

'''

from os import execve
import numpy as np
from sympy import *

# ord_ = number of variables needed for each finite element

def shape_gen(ord_):
    # Constructing symbols for polynomial
    if ord_ / 2 - ord_ // 2 == 0:
        pass
    else:
        raise Exception("ord_ must be an non-negative even number")

    coeff = []
    L = symbols('L')
    for i in range(ord_):
        coeff.append('c' + f'{i}')
    y = symbols('y')
    coeffexpr = []
    for s in coeff:
        globals()[s] = symbols(s)
        coeffexpr.append(symbols(s))
    #print(coeff)
    #print(coeffexpr)

    # Construction for terms in y
    term = []
    e = 0
    while e < len(coeffexpr):
        term.append(coeffexpr[e] * y**e)
        e += 1
    #print(term)

    # Constructing x
    x = 0
    for t in term:
        x += t
    # print(y)
 

    n = ord_ // 2
    Q = []
    for i in range(n):
        k = diff(x, y, i)
        globals()['q'+f'{i}'] = k.subs(y, 0)
        Q.append(k.subs(y,0))
    for i in range(n, ord_):
        k = diff(x, y, i - n)
        globals()['q'+f'{i}'] = k.subs(y, L)
        Q.append(k.subs(y, L))

    # print(Q)
    # print(coeffexpr)
    
    A, b = linear_eq_to_matrix(Q, coeffexpr)
    # print(A)
    # print(b)

    shape_func = []

    A_ = A**-1
    # print(A_)

    for j in range(ord_):
        expr = 0
        for i in range(ord_):
            expr += A_[i, j] * y ** i
        shape_func.append(expr)

    # print(shape_func) 
    return shape_func
    

if __name__ == '__main__':
    y, L = symbols('y, L')
    shape_func = shape_gen(4)
    print(shape_func)
    q1, q1_dot, q2, q2_dot = symbols('q1, q1_dot, q2, q2_dot')
    def dot(v1, v2):
        length = len(v1)
        if len(v2) != length:
            raise Exception("length of v1 and v2 must be equal")
        else:
            local = []
            for i in range(length):
                local.append(v1[i]*v2[i])
            return sum(local)

    q_list = [q1, q1_dot, q2, q2_dot]

    bending = dot(q_list, shape_func)

    bending_int = simplify(integrate(bending, (y, 0, L)))

    print(bending_int)

