import numpy as np
import matplotlib.pyplot as plt
import scipy.misc as spm

def getNodesEqualGap(n, x_range):
    gap = (x_range[1] - x_range[0]) / (n - 1)
    nodes = [node for node in np.arange(x_range[0], x_range[1], gap)]
    nodes.append(x_range[1])
    return nodes

def getNodesCzebyszew(n, x_range):
    centre = (x_range[1] + x_range[0]) / 2
    radius = (x_range[1] - x_range[0]) / 2
    return [(np.cos(((2 * i - 1) / (2 * n)) * np.pi)) * radius + centre for i in range(1, n + 1)]

def getNodesRandom(n, x_range):
    nodes = []
    length = x_range[1] - x_range[0]
    scale = length / (2 * 2.5)
    for i in range(n):
        nodes.append(np.random.normal(0, scale) % length - (length / 2))
    return nodes

def Lagrange(f, n, x_range, step, nodes):
    x_vals = np.arange(x_range[0], x_range[1] + step, step)
    y_vals = []
    
    for x in x_vals:
        w = 0
        for i in range(0, n):
            x_i = nodes[i]
            
            l = 1
            for j in range(0,n):
                if j != i:
                    x_j = nodes[j]
                    l = l * ((x - x_j) / (x_i - x_j))

            w = w + f(x_i) * l
        y_vals.append(w)

    return (np.array(x_vals), np.array(y_vals))

def spline_interpolation(f, n, x_range, step, nodes):
    def findSplite(x_tuple, y_tuple, y_der_tuple):
        x1 = x_tuple[0]
        x2 = x_tuple[1]
        y1 = y_tuple[0]
        y2 = y_tuple[1]
        yd1 = y_der_tuple[0]
        yd2 = y_der_tuple[1]

        t = lambda x: (x - x1) / (x2 - x1)
        a = yd1 * (x2 - x1) - (y2 - y1)
        b = -yd2 * (x2 - x1) + (y2 - y1)

        q = lambda x: (1 - t(x)) * y1 + t(x) * y2 + t(x) * (1 - t(x)) * (a * (1 - t(x)) + b * t(x))

        return q

    if x_range[0] not in nodes:
        nodes.append(x_range[0])
    if x_range[1] not in nodes:
        nodes.append(x_range[1])
    nodes = list(sorted(nodes))

    x_vals = []
    y_vals = []

    for i in range(1, len(nodes)):
        x1 = nodes[i - 1]
        x2 = nodes[i]
        y1 = f(x1)
        y2 = f(x2)
        yd1 = spm.derivative(f, x1)
        yd2 = spm.derivative(f, x2)
        poly = findSplite([x1, x2], [y1, y2], [yd1, yd2])
        for x in np.arange(x1, x2, step):
            x_vals.append(x)
            y_vals.append(poly(x))

    x_vals.append(x_range[1])
    y_vals.append(poly(x_range[1]))

    return (np.array(x_vals), np.array(y_vals))

def main():
    def getError(algorithm, nodesAlgorithm, n):
        sumError = []
        avgError = []
        for i in range(3, n):
            f_interpol = algorithm(f, i, (x_min, x_max), step, nodesAlgorithm(i, (x_min, x_max)))
            sumError.append(abs(sum(f_interpol[0]) - sum(f_interpol[1])))
        for se in sumError:
            avgError.append(se / len(f_interpol[0]))

        return avgError

    def makeFigure(number, title, algorithm, nodesAlgorithm):
        plt.figure(number)
        plt.suptitle(title)
        f_interpol = algorithm(f, 3, (x_min, x_max), step, nodesAlgorithm(3, (x_min, x_max)))
        plt.subplot(221, title="n=3")
        plt.plot(f_interpol[0], f(f_interpol[0]), "b-")
        plt.plot(f_interpol[0], f_interpol[1], "r-")
        f_interpol = algorithm(f, 5, (x_min, x_max), step, nodesAlgorithm(5, (x_min, x_max)))
        plt.subplot(222, title="n=5")
        plt.plot(f_interpol[0], f(f_interpol[0]), "b-")
        plt.plot(f_interpol[0], f_interpol[1], "r-")
        f_interpol = algorithm(f, 9, (x_min, x_max), step, nodesAlgorithm(9, (x_min, x_max)))
        plt.subplot(223, title="n=9")
        plt.plot(f_interpol[0], f(f_interpol[0]), "b-")
        plt.plot(f_interpol[0], f_interpol[1], "r-")

        n = 13
        error = getError(algorithm, nodesAlgorithm, n + 1)
        plt.subplot(224, title="Avg error")
        plt.plot(range(3, n + 1), error, "go")


    f = lambda x: 1 / (1 + 25*x**2)
    x_min = -1.0
    x_max = 1.0
    step = 0.01

    makeFigure(1, "Lagrange - equal gap", Lagrange, getNodesEqualGap)
    makeFigure(2, "Lagrange - Czebyszew", Lagrange, getNodesCzebyszew)
    makeFigure(3, "Splite - equal gap", spline_interpolation, getNodesEqualGap)
    makeFigure(4, "Lagrange - random gap", Lagrange, getNodesRandom)

    plt.show()

if __name__ == "__main__":
    main()