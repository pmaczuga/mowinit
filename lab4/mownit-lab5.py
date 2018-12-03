import numpy as np
import matplotlib.pyplot as plt
import imageio
import random
import math

def acceptance_probability(current_energy, new_energy, T):
	if current_energy < new_energy:
		return 1.0
	return math.exp(-(current_energy - new_energy) / T)

def simulated_annealing(points, T, E, next, cooling_rate):
	history = []
	points = points.copy()
	history.append(points)
	energy1 = E(points)

	while T > 1:
		new_points = next(points)
		current_energy = E(points)
		new_energy = E(new_points)

		if acceptance_probability(current_energy, new_energy, T) > random.random():
			points = new_points
			history.append(points.copy())

		T = T - T * cooling_rate
	energy2 = E(points)
	print(energy2 - energy1)
	return history

# ---------------------------------------------------------------------------------
# --------------------------first-task---------------------------------------------
# ---------------------------------------------------------------------------------

def full_distance(points):
	sum = 0
	for i in range(0, len(points) - 1):
		x1, y1 = points[i]
		x2, y2 = points[i + 1]
		r = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
		sum = sum + r
	return sum

def next_list_permutation(points):
	new_points = points.copy()
	first = 0
	second = 0
	while first == second:
		first = random.randrange(len(new_points))
		second = random.randrange(len(new_points))

	new_points[first], new_points[second] = new_points[second], new_points[first]
	return new_points

def get_points(num, points_range):
	result = []
	start, stop = points_range
	for i in range(num):
		result.append((random.randrange(start, stop), random.randrange(start, stop)))
	return result


# ---------------------------------------------------------------------------------
# --------------------------second-task--------------------------------------------
# ---------------------------------------------------------------------------------


def gravitation_energy(down_force, between_froce):
	def wrapper(array):
		def distance(first, second):
			x1, y1 = first
			x2, y2 = second
			return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

		energy = 0
		for i in range(array.shape[0]):
			for j in range(array.shape[1]):
				for k in range(i + 1, array.shape[0]):
					for l in range(j + 1, array.shape[1]):
						if array[i][j] == 0:
							energy = energy + down_force
							if array[k][l] == 0:
								energy = energy + (between_froce / distance((i, j), (k, l)))
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

def get_rand_array(size, probabilty):
	array = np.zeros((size, size), dtype=np.uint8)
	for i in range(size):
		for j in range(size):
			if random.random() > probabilty:
				array[i][j] = 255
	return array

# ---------------------------------------------------------------------------------
# --------------------------main---------------------------------------------------
# ---------------------------------------------------------------------------------

def main():
	# points = get_points(100, (0, 100))
	# simulated_annealing(points, 10, full_distance, next_list_permutation, 0.001)

	array = get_rand_array(20, 0.2)
	images = simulated_annealing(array, 100, gravitation_energy(10, 100), next_array_permutation, 0.001)

	imageio.imsave("gravity1.png", images[0])
	imageio.imsave("gravity2.png", images[-1])
	imageio.mimsave("gravity.gif", images)

if __name__ == "__main__":
	main()