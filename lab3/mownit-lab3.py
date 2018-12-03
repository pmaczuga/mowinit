from math import *

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

print(falsi(k, (-10,0), 1000000, 10e-8))
print(bisection(k, (-10,10), 1000000, 10e-8))
