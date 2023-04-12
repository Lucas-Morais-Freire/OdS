from fractions import *
from IPython.display import Image
from IPython.display import display

def formula_as_file(formula):
    return Image(url=r'http://latex.codecogs.com/png.latex?\dpi{150} %s' % formula)

def copyMatrix(m):
    m2 = []
    for i in range(len(m)):
        m2.append([])
    for i in range(len(m)):
        for j in range(len(m[0])):
            m2[i].append(m[i][j])
    return m2

def makeMatrix(z, r, min=False):
    Z = []
    n = len(z[0])
    nr = len(r) + 1
    for i in range(n):
        Z.append(-z[0][i])
        if not z[1][i]:
            Z.append(z[0][i])
    n = len(Z)
    if min:
        Z = [-i for i in Z]
    m = []
    for i in range(nr):
        m.append([])
        for j in range(n + nr):
            m[i].append(Fraction(0,1))
    for i in range(n):
        m[0][i] = Fraction(Z[i], 1)
    for i in range(1, nr):
        track = 0
        for j in range(len(z[0])):
            if r[i - 1][-2] == '>=':
                m[i][j + track] = Fraction(-r[i - 1][j], 1)
                if not z[1][j]:
                    m[i][j + 1 + track] = Fraction(r[i - 1][j], 1)
                    track += 1
            else:
                m[i][j + track] = Fraction(r[i - 1][j], 1)
                if not z[1][j]:
                    m[i][j + 1 + track] = Fraction(-r[i - 1][j], 1)
                    track += 1
    for i in range(nr - 1):
        if r[i][-2] == '>=':
            m[i + 1][-1] = Fraction(-r[i][-1], 1)
        else:
            m[i + 1][-1] = Fraction(r[i][-1], 1)
        
    for i in range(nr - 1):
        m[i + 1][i + n] = Fraction(1, 1)
    art = 0
    for i in range(nr):
        if m[i][-1] < 0:
            art += 1
    if art != 0:
        for i in range(nr):
            for j in range(art):
                m[i].insert(- 1, Fraction(0, 1))
        art = 0
        for i in range(nr):
            if m[i][-1] < 0:
                m[i][n + nr + art - 1] = Fraction(-1, 1)
                art += 1
        for i in range(len(m[0])):
            m[0][i] = Fraction(0, 1) if (i < n + nr - 1 or i == len(m[0]) - 1) else Fraction(1,1)
    return m

def lineOperation(m, i1:int, C1:Fraction=Fraction(1,1), i2:int=0, C2:Fraction=Fraction(0,1)):
    c1 = C1 if C1.denominator == 1 else (f'{"-" if C1 < 0 else ""}' + '\\frac{' + str(abs(C1.numerator)) + '}{' + str(C1.denominator) + '}')
    c2 = C2 if C2.denominator == 1 else (f'{"-" if C1 < 0 else ""}' + '\\frac{' + str(abs(C2.numerator)) + '}{' + str(C2.denominator) + '}')
    img = formula_as_file('L_{' + str(i1) + '} \\rightarrow ' + f'{c1 if C1 != 1 and C1 != -1 else ("-" if C1 == -1 else "")}' + 'L_{' + str(i1) + '}' + f'{"+" if C2 > 0 else ("-" if C2 < 0 else "")} {c2 if (C2 > 0 and C2 != 1) else (str(c2) if (C2 < 0 and C2 != -1) else "")}' + f'{"L_{" if C2 != 0 else ""}' + f'{i2 if C2 != 0 else ""}' + f'{"}" if C2 != 0 else ""}')
    display(img)
    for j in range(len(m[0])):
        m[i1][j] = C1*m[i1][j] + C2*m[i2][j]

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

def printTable(m:list[list[Fraction]], z, label='z'):
    expr = f'\\begin{{array}}{"{"}c|c|'
    for i in range(len(m[0]) - 1):
        expr += 'c'
    expr += f'|c{"}"} \n & {label}'
    k = 0
    for i in range(len(z[0])):
        expr += f' & x_{"{"}{i + 1}{"}"}'
        if not z[1][i]:
            expr += f'\' & x_{"{"}{i + 1}{"}"}\'\''
            k += 1
    for i in range(len(z[0]) + 1, len(m[0]) - k):
        expr += f' & x_{"{"}{i}{"}"}'
    expr += ' & b \\\ \n\hline\n q & 1'
    for i in range(len(m[0])):
        expr += ' & ' + (f'{m[0][i]}' if m[0][i].denominator == 1 else f'\\frac{"{"}{m[0][i].numerator}{"}"}{"{"}{m[0][i].denominator}{"}"}')
    expr += ' \\\ \n'
    mindex = m[0][:-1].index(min(m[0][:-1]))
    for i in range(1, len(m)):
        qn = m[i][-1].numerator*m[i][mindex].denominator
        qd = m[i][-1].denominator*m[i][mindex].numerator
        expr += f'{qn} \\slash {qd} & 0'
        for j in range(len(m[0])):
            expr += ' & ' + (f'{m[i][j]}' if m[i][j].denominator == 1 else f'\\frac{"{"}{m[i][j].numerator}{"}"}{"{"}{m[i][j].denominator}{"}"}')
        expr += ' \\\ \n'
    expr += '\\end{array}'
    return formula_as_file(expr)

def makePivot(m, i, j, z, label):
    C = Fraction(1,1)/m[i][j]
    lineOperation(m, i, C)
    display(printTable(m, z, label))
    for k in range(len(m)):
        if k != i:
            C = -m[k][j]
            lineOperation(m, k, i2=i, C2=C)

def printQValues(m, j):
    for i in range(1, len(m)):
        print((m[i][-1]/m[i][j]).numerator/(m[i][-1]/m[i][j]).denominator)

def putBack(m:list[list[Fraction]], z, min=False):
    Z = []
    n = len(z[0])
    for i in range(n):
        Z.append(-z[0][i])
        if not z[1][i]:
            Z.append(z[0][i])
    for i in range(len(Z)):
        m[0][i] = Fraction(Z[i], 1)
    for i in range(len(Z), len(m[0])):
        m[0][i] = Fraction(0,1)