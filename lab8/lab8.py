import numpy as np
from PIL import Image
import scipy.misc as sp

im = Image.open('noise.bmp')

# get image
before = np.array(im)

# DFT
after = np.fft.fft2(before)

# change

after = after[0:-2,:]

# avg = np.average(abs(after))
# for i in range(after.shape[0]):
# 	for j in range(after.shape[1]):
# 		if(abs(after[i][j]) < avg):
# 			after[i][j] = 0


# IDFT
back = np.fft.ifft2(after)
back = np.abs(back)

sp.imsave('res.bmp', back)
