import numpy as np
import matplotlib.pyplot as plt
import imageio
import random
import math
import copy

def acceptance_probability(current_energy, new_energy, T):
    if new_energy < current_energy:
        return 1.0
    return math.exp((current_energy - new_energy) / T)

def simulated_annealing(data, E, next, n=10000, m=100, T=5, cooling_rate=0.001):
    data = copy.deepcopy(data)

    for i in range(n):
        for j in range(m):
            new_data = next(data)
            current_energy = E(data)
            new_energy = E(new_data)

            if acceptance_probability(current_energy, new_energy, T) > random.random():
                data = new_data
                if new_energy == 0:
                    print("Solution found after: ", i, "iterations")
                    return data
        
        T = T - T * cooling_rate

    print("Didn't find the solution")
    return data

class Sudoku():
    def __init__(self, input = None):
        if input is None:
            self.input = np.full((9,9), 0)
        else:
            self.input = input

        self.fill_random()

    def __str__(self):
        return str(self.output)

    def fill_random(self):
        self.output = self.input.copy()
        for i in range(9):
            to_fill = set((1,2,3,4,5,6,7,8,9)).difference(set(self.output[i,:]))
            for j in range(9):
                if self.output[i,j] == 0:
                    self.output[i,j] = to_fill.pop()
        
    def can_change(self, x, y):
        return self.input[x][y] == 0

    def get_rows(self):
        data = self.output.copy()
        return [list(data[i,:]) for i in range(9)]

    def get_columns(self):
        data = self.output.copy()
        return [list(data[:,i]) for i in range(9)]

    def get_squares(self):
        data = self.output.copy()
        squares = [[] for i in range(9)]
        for i in range(9):
            for j in range(9):
                squares[i//3 + (j//3)*3].append(data[i][j])
        return squares

def get_energy(sudoku):
    sub_val = 1
    add_val = 1
    energy = 0

    for co_ro_sq in [sudoku.get_columns(), sudoku.get_squares()]:
        for tmp in co_ro_sq:
            energy = energy + add_val * (9 - len(set(tmp)))
    return energy

def next_perm(sudoku):
    sudoku = copy.deepcopy(sudoku)
    
    while True:
        row = random.randrange(0,9)
        for i in range(4):
            x1 = random.randrange(0,9)
            x2 = random.randrange(0,9)            
            if sudoku.can_change(row, x1) and sudoku.can_change(row, x2):
                sudoku.output[row][x1], sudoku.output[row][x2] = sudoku.output[row][x2], sudoku.output[row][x1]
                return sudoku

def main():
    
    data = np.array([[5,3,0,0,7,0,0,0,0],
                      [6,0,0,1,9,5,0,0,0],
                      [0,9,8,0,0,0,0,6,0],
                      [8,0,0,0,6,0,0,0,3],
                      [4,0,0,8,0,3,0,0,1],
                      [7,0,0,0,2,0,0,0,6],
                      [0,6,0,0,0,0,2,8,0],
                      [0,0,0,4,1,9,0,0,5],
                      [0,0,0,0,8,0,0,7,9]])

    sudoku = Sudoku(data)
    print(sudoku.input)

    sudoku = simulated_annealing(
        sudoku, 
        get_energy, 
        next_perm, 
        n=50, 
        m=6500, 
        T=10, 
        cooling_rate=0.1)

    print(sudoku)
    print("End energy: ", get_energy(sudoku))

if __name__ == "__main__":
    main()