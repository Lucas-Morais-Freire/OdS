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
        for j in range(len(m[i])):
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
        for j in range(n):
            m[i].append(Fraction(0,1))
    for i in range(n):
        m[0][i] = Fraction(Z[i])
    m[0].append(Fraction(0,1))
    for i in range(1, nr):
        neg = 0
        for j in range(len(z[0])):
            if r[i - 1][-2] == '<=':
                m[i][j + neg] = Fraction(r[i - 1][j], 1)
                if not z[1][j]:
                    m[i][j + 1 + neg] = Fraction(-r[i - 1][j], 1)
                    neg += 1
            elif r[i - 1][-2] == '>=':
                m[i][j + neg] = Fraction(-r[i - 1][j], 1)
                if not z[1][j]:
                    m[i][j + 1 + neg] = Fraction(r[i - 1][j], 1)
                    neg += 1
            elif r[i - 1][-2] == '=':
                if r[i - 1][-1] < 0:
                    m[i][j + neg] = Fraction(-r[i - 1][j], 1)
                    if not z[1][j]:
                        m[i][j + 1 + neg] = Fraction(r[i - 1][j], 1)
                        neg += 1
                else:
                    m[i][j + neg] = Fraction(r[i - 1][j], 1)
                    if not z[1][j]:
                        m[i][j + 1 + neg] = Fraction(-r[i - 1][j], 1)
                        neg += 1
        if r[i - 1][-2] == '<=':
            m[i].append(Fraction(r[i - 1][-1], 1))
        elif r[i - 1][-2] == '>=':
            m[i].append(Fraction(-r[i - 1][-1], 1))
        elif r[i - 1][-2] == '=':
            if r[i - 1][-1] < 0:
                m[i].append(Fraction(-r[i - 1][-1], 1))
            else:
                m[i].append(Fraction(r[i - 1][-1], 1))
    for i in range(1, nr):
        if r[i - 1][-2] != '=':
            m[0].append(Fraction(0,1))
            for j in range(1, nr):
                if j == i:
                    m[j].insert(-1, Fraction(1,1))
                else:
                    m[j].insert(-1, Fraction(0,1))
    twoStep = False
    for i in range(1, nr):
        if m[i][-1] < 0:
            twoStep = True
            m[0].insert(-1, Fraction(1,1))
            for j in range(1, nr):
                if j == i:
                    m[j].insert(-1, Fraction(-1, 1))
                else:
                    m[j].insert(-1, Fraction(0, 1))
    if twoStep:
        for i in range(n):
            m[0][i] = Fraction(0,1)
    return m

def lineOperation(m, i1:int, C1:Fraction=Fraction(1,1), i2:int=0, C2:Fraction=Fraction(0,1)):
    c1 = C1 if C1.denominator == 1 else (f'{"-" if C1 < 0 else ""}' + '\\frac{' + str(abs(C1.numerator)) + '}{' + str(C1.denominator) + '}')
    c2 = C2 if C2.denominator == 1 else (f'{"-" if C2 < 0 else ""}' + '\\frac{' + str(abs(C2.numerator)) + '}{' + str(C2.denominator) + '}')
    #img = formula_as_file('L_{' + str(i1) + '} \\rightarrow ' + f'{c1 if C1 != 1 and C1 != -1 else ("-" if C1 == -1 else "")}' + 'L_{' + str(i1) + '}' + f'{"+" if C2 > 0 else ""} {c2 if (C2 > 0 and C2 != 1) else (str(c2) if (C2 < 0 and C2 != -1) else "")}' + f'{"L_{" if C2 != 0 else ""}' + f'{i2 if C2 != 0 else ""}' + f'{"}" if C2 != 0 else ""}')
    img = formula_as_file(f'L_{"{"}{str(i1)}{"}"} \\rightarrow ' + ('' if C1 == 1 else ('-' if C1 == -1 else str(c1))) + f'L_{"{"}{str(i1)}{"}"}' + ('+' if C2 > 0 else '') + ('' if C2 == 1 or C2 == 0 else ('-' if C2 == -1 else str(c2))) + (f'L_{"{"}{str(i2)}{"}"}' if C2 != 0 else ''))
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

def printTable(m:list[list[Fraction]], z, label='z', varSubs=None):
    expr = f'\\begin{{array}}{"{"}c|c|'
    for i in range(len(m[0]) - 1):
        expr += 'c'
    expr += f'|c{"}"} \n & {label}'
    k = 0
    for i in range(len(z[0])):
        if varSubs != None:
            expr += f' & x_{"{"}{varSubs[i]}{"}"}'
        else:
            expr += f' & x_{"{"}{i + 1}{"}"}'
        if not z[1][i]:
            if varSubs != None:
                expr += f'\' & x_{"{"}{varSubs[i]}{"}"}\'\''
            else:
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

def makePivot(m, i, j, z, label='z', varSubs=None):
    C = Fraction(1,1)/m[i][j]
    lineOperation(m, i, C)
    display(printTable(m, z, label, varSubs))
    for k in range(len(m)):
        if k != i:
            C = -m[k][j]
            lineOperation(m, k, i2=i, C2=C)

def printQValues(m, j):
    for i in range(1, len(m)):
        print((m[i][-1]/m[i][j]).numerator/(m[i][-1]/m[i][j]).denominator)

def putBack(m:list[list[Fraction]], z, r, min=False):
    r2 = copyMatrix(r)
    for row in r2:
        if row[-2] == "<=" and row[-1] < 0:
            row[-1] = -row[-1]
        elif row[-2] == ">=" and row[-1] > 0:
            row[-1] = -row[-1]
        elif row[-2] == '=' and row[-1] < 0:
            row[-1] = -row[-1]
    m2 = makeMatrix(z, r2, min)
    for i in range(1, len(m2)):
        for j in range(len(m2[i]) - 1):
            m2[i][j] = m[i][j]
    for i in range(1, len(m2)):
        m2[i][-1] = m[i][-1]
    return m2