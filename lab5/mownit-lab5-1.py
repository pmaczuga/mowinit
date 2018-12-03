import numpy as np
import matplotlib.pyplot as plt
import imageio
import random
import math
import itertools
import time

def acceptance_probability(current_energy, new_energy, T):
	if new_energy < current_energy:
		return 1.0
	return math.exp((current_energy - new_energy) / T)

def simulated_annealing(points, T, E, next, cooling_rate):
	points = points.copy()
	energy1 = E(points)

	while T > 1:
		new_points = next(points)
		current_energy = E(points)
		new_energy = E(new_points)

		if acceptance_probability(current_energy, new_energy, T) > random.random():
			points = new_points

		T = T - T * cooling_rate
	energy2 = E(points)

	energy_difference = (energy1 - energy2)
	return (points, energy_difference)

def precise_algorithm(points, E):
	energy1 = E(points)
	best_energy = energy1
	best_points = points.copy()
	for permutation in itertools.permutations(points):
		energy = E(permutation)
		if energy < best_energy:
			best_energy = energy
		best_points = permutation

	return (list(best_points), best_energy)


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


def main():
	points = get_points(10, (0, 100))

	print(full_distance(points))
	
	start1 = time.time()
	points1, difference1 = simulated_annealing(points, 10, full_distance, next_list_permutation, 0.001)
	stop1 = time.time()
	print("Time annealing: ", stop1 - start1, "   energy difference: ", difference1)

	start2 = time.time()
	points2, difference2 = precise_algorithm(points, full_distance, )
	stop2 = time.time()
	print("Time precise: ", stop2 - start2, "   energy difference: ", difference2)

if __name__ == "__main__":
	main()