import numpy as np
import matplotlib.pyplot as plt

f = lambda x: 1 / (1 + 25*x**2)

n = 7
x_range = (-5.0, 5.0)

step = (x_range[1] - x_range[0]) / (n - 1)
points = [point for point in np.arange(x_range[0], x_range[1], step)]
points.append(x_range[1])

l = [lambda x: 1 for i in range(n)]

w = lambda x: 0
for i in range(0, n):
    x_i = points[i]
    
    for j in range(0,n):
        if j != i:
            x_j = points[j]
            l[i] = lambda x, k = l[i]: k(x) * ((x - x_j) / (x_i - x_j))

    w = lambda x, k = w: k(x) + f(points[i]) * l[i](x)

print(l[3](points[6]))


t = np.arange(x_range[0], x_range[1], 0.001)

plt.figure(3)
plt.plot(t, l[2](t))

plt.figure(1)
plt.plot(t, f(t))

plt.figure(2)
plt.plot(t, w(t))

plt.show()