import numpy as np
from PIL import Image
import scipy.misc as sp


im = Image.open('in.png')

array = np.array(im)

print(array.shape)