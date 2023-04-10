import numpy as np
from fractions import *

def makeMatrix(z, r, min=False):
    Z = []
    n = len(z[0])
    nr = len(r) + 1
    for i in range(n):
        Z.append(-z[0][i])
        if not z[1][i]:
            Z.append(z[0][i])
    if min:
        z = -z
    m = []
    for i in range(nr):
        m.append([])
        for j in range(n + nr):
            m[i].append(Fraction(0,1))
    for i in range(n):
        m[0][i] = Fraction(Z[i], 1)
    for i in range(1, nr):
        for j in range(n):
            if r[i - 1][-2] == '>=':
                m[i][j] = Fraction(-r[i - 1][j], 1)
            else:
                m[i][j] = Fraction(r[i - 1][j], 1)
    for i in range(nr - 1):
        if r[i][-2] == '>=':
            m[i + 1][-1] = Fraction(-r[i][-1], 1)
        else:
            m[i + 1][-1] = Fraction(r[i][-1], 1)
        
    for i in range(nr - 1):
        m[i + 1][i + n] = Fraction(1, 1)
    return m

def makePivot(m, i, j):
    C = Fraction(1,1)/m[i][j]
    for k in range(len(m[0])):
        m[i][k] =C*m[i][k]
    for k in range(len(m)):
        if k != i:
            C = -m[k][j]
            for l in range(len(m[0])):
                m[k][l] = m[k][l] + C*m[i][l]

def printMatrix(m):
    M = []
    for i in range(len(m)):
        M.append([])
        for j in range(len(m[0])):
            M[i].append(str(m[i][j]))

    for j in range(len(M[0])):
        mLen = len(M[0][j])
        for i in range(len(M)):
            if len(M[i][j]) > mLen:
                mLen = len(M[i][j])
        for i in range(len(M)):
            while len(M[i][j]) != mLen:
                M[i][j] = ' ' + M[i][j]
    for i in range(len(M)):
        print('[', sep='', end='')
        for j in range(len(M[0]) - 1):
            print(M[i][j],', ', sep='', end='')
        print(M[i][-1],']', sep='')
    print('')

def printQValues(m, j):
    for i in range(1, len(m)):
        print((m[i][-1]/m[i][j]).numerator/(m[i][-1]/m[i][j]).denominator)

z = [[3, 2, 5], [True, True, True]]
r = [[2, 3, 4,'<=', 10],
     [5, 6, 2,'<=', 12]]

m = makeMatrix(z, r)

printMatrix(m)

printQValues(m, 2)