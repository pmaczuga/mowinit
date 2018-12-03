import numpy as np
import matplotlib.pyplot as plt
import imageio
import random
import math

def acceptance_probability(current_energy, new_energy, T):
	if new_energy < current_energy:
		return 1.0
	return math.exp((current_energy - new_energy) / T)

def simulated_annealing(data, E, next, T=100, cooling_rate=0.01):
	history = []
	data = data.copy()
	history.append(data)
	energy1 = E(data)

	while T > 1:
		new_data = next(data)
		current_energy = E(data)
		new_energy = E(new_data)

		if acceptance_probability(current_energy, new_energy, T) > random.random():
			data = new_data
			history.append(data.copy())

		T = T - T * cooling_rate
	energy2 = E(data)
	print(energy1 - energy2)
	return history


def gravitation_energy(posistion_fun, between_fun):
	def wrapper(array):
		def distance(first, second):
			x1, y1 = first
			x2, y2 = second
			return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

		energy = 0
		length = array.shape[1]
		height = array.shape[0]
		diagonal  = distance((0, 0), (length, height))
		for i in range(height):
			for j in range(length):
				if array[i][j] == 0:
					energy = energy + posistion_fun(i / height, j / length)
					for k in range(height):
						for l in range(length):
							if i != k and j != l and array[k][l] == 0:
								energy = energy + between_fun(distance((i, j), (k, l)) / diagonal)
		return energy

	return wrapper


def next_array_permutation(array):
	array = array.copy()
	x1, x2, y1, y2 = (0,0,0,0)
	while array[x1][y1] == array[x2][y2]:
		x1 = random.randrange(array.shape[0])
		x2 = random.randrange(array.shape[0])
		y2 = random.randrange(array.shape[1])
		y1 = random.randrange(array.shape[1])
	array[x1][y1], array[x2][y2] = array[x2][y2], array[x1][y1]
	return array


def get_rand_array(size, probability=0.5):
	array = np.zeros((size, size), dtype=np.uint8)
	for i in range(size):
		for j in range(size):
			if random.random() > probability:
				array[i][j] = 255
	return array


def main():
	# create random array
	array = get_rand_array(20, probability=0.15)

	# calculates energy based on points position
	posistion_fun = lambda y, x: 500 * (math.sin(y * math.pi + math.pi) + math.sin(x * math.pi + math.pi))
	# calculates energy based on distance from other points
	between_fun = lambda r: -20 * r
	# energy is based on both previous functions
	gravitation_fun = gravitation_energy(posistion_fun, between_fun)

	images = simulated_annealing(array, gravitation_fun, next_array_permutation, T=100, cooling_rate=0.003)

	imageio.imsave("gravity1.png", images[0])
	imageio.imsave("gravity2.png", images[-1])
	imageio.mimsave("gravity.gif", images)

if __name__ == "__main__":
	main()