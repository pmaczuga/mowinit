import numpy as np
from PIL import Image
import PIL.ImageOps
import scipy.misc as sp
import scipy.signal as sig
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# const
show_letter = 'a'
letters_path = 'arial/'
alphabet = 'abcdefghijklmnopqrstuvwxyz'
eps = 0.99
line_eps = 5

# prepare
letters = dict()
result = dict()
string_result = ''
fig, axes = plt.subplots(1, 3)

# load text and letters
text = (Image.open('text.png')).convert('L')
for letter in alphabet:
	letters[letter] = (Image.open(letters_path + letter + '.png')).convert('L')


# invert colors
text = PIL.ImageOps.invert(text)
for letter in alphabet:
	letters[letter] = PIL.ImageOps.invert(letters[letter])

# to array
text = np.array(text)
for letter in alphabet:
	letters[letter] = np.array(letters[letter])

axes[0].imshow(text, cmap='gray')
axes[1].imshow(letters[show_letter], cmap='gray')

# normalize
text = text/255
for letter in alphabet:
	letters[letter] = letters[letter]/255

# flip
for letter in alphabet:
	letters[letter] = np.flip(letters[letter])

# convolve, save to dict (point -> letter)
output = dict()
for letter in alphabet:
	output[letter] = sig.fftconvolve(text, letters[letter], mode="valid")
	output[letter] = (output[letter]-np.min(output[letter]))/(np.max(output[letter])-np.min(output[letter]))
	for i in range(output[letter].shape[0]):
		for j in range(output[letter].shape[1]):
			if output[letter][i,j] > eps:
				result[(i,j)] = letter

#sort result by lines (with some room for error)
sorted_keys = dict()
for point in result.keys():
	for key in sorted_keys.keys():
		if abs(key - point[0]) < line_eps:
			sorted_keys[key].append(point)
			break
	else:
		sorted_keys[point[0]] = list()
		sorted_keys[point[0]].append(point)


def only_second(x):
	return x[1]

# write as string
for line in sorted(sorted_keys.keys()):
	for point in sorted(sorted_keys[line], key=only_second):
		string_result += result[point]
		print(point, ': ', result[point])
	string_result += '\n'

axes[2].imshow(output[show_letter], cmap='gray')

print("\nRESULT:")
print(string_result)
plt.show()
