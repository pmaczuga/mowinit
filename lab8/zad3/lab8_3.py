import numpy as np
from PIL import Image
import scipy.misc as sp
import scipy.signal as sig
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, axes = plt.subplots(1, 3)

# load image and kernel (template)
in_image = np.array((Image.open("in.png")).convert('L'))
kernel = np.array((Image.open("lenna_kernel.png")).convert('L'))

# normalize
in_image = in_image/255
kernel = kernel/255


k1 = np.array([
	[-1, 0, 1],
	[-1,0,1],
	[-1,0,1]
	])

k2 = np.array([
	[-1,-1,-1],
	[0,0,0],
	[1,1,1]
	])

im = in_image
# only thing that worked for me is to transform image first
# im = sig.fftconvolve(im, k1, mode="same") + sig.fftconvolve(im, k2, mode="same")
# kernel = sig.fftconvolve(kernel, k1, mode="same") + sig.fftconvolve(kernel, k2, mode="same")
# and do that:
kernel = np.flip(kernel)
# as I understand rotating template makes convultion work the same as cross correlation
# couldn't find other way to locate a template 

axes[0].imshow(im, cmap='gray')

# ------------------------------------------------------------------------
# actual convultion
# output = sig.correlate(im, kernel, mode="valid")
output = sig.fftconvolve(im, kernel, mode="valid")
# ------------------------------------------------------------------------

# crop output a bit - white squares in edges
crop_val = 1
output = output[crop_val:-crop_val, crop_val:-crop_val]
print("output: ", output.shape)
print("kernel: ", kernel.shape)

# find maximum
max_index = np.unravel_index(np.argmax(output), output.shape)
print("max index: ", max_index)

# noramilize
output = (output-np.min(output))/(np.max(output)-np.min(output))
print("Value at max: ", output[max_index])


# when plotting coordinates in plot are shifted a bit (don't know why)
# only plotting output
strange_const = 6

#show convulted image
axes[1].imshow(output, cmap='gray')
width = kernel.shape[1]
height = kernel.shape[0]
x = max_index[0] - width//2 + strange_const			
y = max_index[1] - height//2 - strange_const			
rect = patches.Rectangle((y,x), width, height, linewidth=1,edgecolor='r',facecolor='none')
axes[1].add_patch(rect)


# show real image (black and white) and add rectangle at templete match
axes[2].imshow(in_image, cmap='gray')
width = kernel.shape[1]
height = kernel.shape[0]
x = max_index[0] + crop_val
y = max_index[1] + crop_val
rect = patches.Rectangle((y,x),width,height,linewidth=1,edgecolor='r',facecolor='none')
axes[2].add_patch(rect)

plt.show()
