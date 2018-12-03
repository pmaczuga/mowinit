import numpy as np
import scipy.linalg
from mpl_toolkits.mplot3d import Axes3D
import random
from matplotlib import pyplot
import copy

def generate_cloud(num):
	def withinSphere(point):
		return np.linalg.norm(point) <= 1.0

	result = np.empty([num, 3])

	i = 0
	while i < num - 1:
		point = (
			random.random() * 2.0 - 1.0,
			random.random() * 2.0 - 1.0,
			random.random() * 2.0 - 1.0
			)

		if withinSphere(point):
			i += 1
			result[i,0] = point[0]
			result[i,1] = point[1]
			result[i,2] = point[2]

	return result

def getMatrix(num):
	result = np.empty([num, 3])
	for row in result:
		row[0] = 0.0
		row[1] = 0.0
		row[2] = 0.5
	return result

def transform(points, matrix):
	points = copy.copy(points)


	for i in range(points.shape[0]):
		points[i] = matrix @ points[i]

	return points

def draw_3d_points(points):
	fig = pyplot.figure()
	ax = Axes3D(fig)

	ax.scatter(points.transpose()[0], points.transpose()[1], points.transpose()[2])
	pyplot.show()

def main():

    points = generate_cloud(1000)
    draw_3d_points(points)
    points = transform(points, getMatrix(1000))
    draw_3d_points(points)

if __name__ == "__main__":
    main()