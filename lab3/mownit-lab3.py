from math import *
import random
import scipy.misc as scpm

f = lambda x: x**2 - 2.71 * x + 1
g = lambda x: sin(x - pi/2) * e**(-x * sin(x))
h = lambda x: (1/cos(x))**2 - 1
k = lambda x: 2 + 0.5 * cos(x) - x/3

def bisection(f, borders, iters, precison):
    a,b = borders
    if f(a) * f(b) > 0:
        print("Error!")
    for i in range(iters):
        x0 = (a + b) / 2
        if abs(f(x0)) < precison:
            return x0
        if f(a) * f(x0) < 0:
            b = x0
        else:
            a = x0

    return x0

def falsi(f, borders, iters, precison):
    a,b = borders
    if f(a) * f(b) > 0:
        print("Error!")
    for i in range(iters):
        x0 = a - f(a) * (b - a)/(f(b) - f(a))
        x0 = (a + b) / 2
        if abs(f(x0)) < precison:
            return x0
        if f(a) * f(x0) < 0:
            b = x0
        else:
            a = x0

    return x0

def newton(f, borders, iters, max_diff):
    x0 = 5
    for i in range(iters):
        x1 = x0 - f(x0) / 1


def gradient(fun, k=0.3, l=0.2, eps=10e-6):
    arg = 30

    der = scpm.derivative(fun, arg)
    m = 0
    while(abs(der) >  eps):
        arg_new = arg - der*k + m*l
        m = arg_new - arg
        der = scpm.derivative(fun, arg_new)
        arg = arg_new
        print(arg)
    return arg

def main():
    # print(falsi(k, (-10,0), 1000000, 10e-8))
    # print(bisection(k, (-10,10), 1000000, 10e-8))

    fun = lambda x: -sin(x) * 0.1 * x + 0.01*x**2
    print(gradient(fun, k=0.7, l=0.9, eps=10e-6))
    print("DONE")

main()
