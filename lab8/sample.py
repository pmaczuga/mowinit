import numpy as np
from PIL import Image
import scipy.misc as sp

im = Image.open('noise.png')

before = np.array(im)
after = np.empty((before.shape[0], before.shape[1]))

for i in range(before.shape[0]):
	for j in range(before.shape[1]):
		after[i][j] = before[i][j][0]

sp.imsave("noise.bmp", after)