import numpy as np

def f(x:list[float])->float:
    return pow(x[0],2) - np.sin(x[1]) + 1

def G(x:list[float])->np.ndarray[float]:
    return np.array([[2*x[0]], [-np.cos(x[1])]])

def H(x:list[float])->np.ndarray[float]:
    return np.array([[2, 0], [0, np.sin(x[1])]])

#def Q(x:list[float],x0:list[float])->float:
#    return f(x)+np.transpose(G(x0))*np.array(x-x0)+0.5*np.transpose(x-x0)*H(x0)*(x-x0)

