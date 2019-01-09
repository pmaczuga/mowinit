import numpy as np
import wikipedia

wikipedia.set_lang("en")
pages = wikipedia.random(10)
num_of_words = dict()
vectors = dict()

for title in pages:
	try:
		page = wikipedia.page(title)
	except wikipedia.exceptions.DisambiguationError as e:
		page = e.options[0]
	for word in page.content.split(" "):
		num_of_words[word] = num_of_words.setdefault(word, 0) + 1

i = 0
length = len(num_of_words)
for word in num_of_words.keys():
	vector_as_list = [0 for j in range(length)]
	vector_as_list[i] = 1
	vectors[word] = tuple(vector_as_list)
	i += 1

print(num_of_words["the"])