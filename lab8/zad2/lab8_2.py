import numpy as np
from PIL import Image
import scipy.misc as sp

Q = np.array([
	[16, 11, 10, 16, 24, 40, 51, 61],
	[12, 12, 14, 19, 26, 58, 60, 44],
	[14, 13, 16, 24, 40, 57, 69, 56],
	[14, 17, 22, 29, 51, 87, 80, 52],
	[18, 22, 37, 56, 68, 109, 103, 77],
	[25, 35, 55, 64, 82, 104, 113, 92],
	[49, 64, 78, 87, 103, 121, 120, 101],
	[72, 92, 95, 98, 112, 100, 103, 99]
	])

im = Image.open('in.png')

array = np.array(im)

# ------------------ENCODE----------------------------------

blocks = np.empty((array.shape[0]//8, array.shape[1]//8, 8, 8, 3))

# convert image to 8x8 blocks in YCbCr
for i in range(array.shape[0]):
	for j in range(array.shape[1]):
		R = array[i][j][0]
		G = array[i][j][1]
		B = array[i][j][2]
		blocks[i//8][j//8][i%8][j%8][0] = 0.299 * R + 0.587 * G + 0.114 * B
		blocks[i//8][j//8][i%8][j%8][1] = -0.1687 * R - 0.3133 * G + 0.5 * B + 128
		blocks[i//8][j//8][i%8][j%8][2] = 0.5 * R - 0.4187 * G - 0.0813 * B + 128


# FFT and quantization
afterFFT = np.empty_like(blocks, dtype=np.complex64)
for k in range(blocks.shape[0]):
	for l in range(blocks.shape[1]):
		block = np.fft.fft2(blocks[k][l])
		for i in range(8):
			for j in range(8):
				block[i][j][0] = block[i][j][0]/Q[i][j]
				block[i][j][1] = block[i][j][1]/Q[i][j]
				block[i][j][2] = block[i][j][2]/Q[i][j]
		afterFFT[k][l] = block

#-------------------------DECODE--------------------------

# dequantization
for k in range(blocks.shape[0]):
	for l in range(blocks.shape[1]):
		for i in range(8):
			block = afterFFT[k][l]
			for j in range(8):
				block[i][j][0] = block[i][j][0]*Q[i][j]
				block[i][j][1] = block[i][j][1]*Q[i][j]
				block[i][j][2] = block[i][j][2]*Q[i][j]
		afterFFT[k][l] = block

# IFFT
afterIFFT = np.empty_like(blocks)
for k in range(blocks.shape[0]):
	for l in range(blocks.shape[1]):
		afterIFFT[k][l] = np.abs(np.fft.ifft2(afterFFT[k][l]))

output = np.empty(array.shape)

# convert back to RGB array
for i in range(output.shape[0]):
	for j in range(output.shape[1]):
		Y = afterIFFT[i//8][j//8][i%8][j%8][0]
		Cb = afterIFFT[i//8][j//8][i%8][j%8][1]
		Cr = afterIFFT[i//8][j//8][i%8][j%8][2]
		output[i][j][0] = Y + 1.402 * (Cr - 128)
		output[i][j][1] = Y - 0.3441 * (Cb - 128) - 0.7141 * (Cr - 128)
		output[i][j][2] = Y + 1.772 * (Cb - 128)


# save result
sp.imsave("out.png", output)