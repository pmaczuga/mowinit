import wikipedia

number = 80
min_length = 10000
filename = "Pages titles.txt"

wikipedia.set_lang("en")
file = open(filename, "a")
file.close()
file = open(filename, "a")

i = 0
while True:
	title = wikipedia.random(1)
	try:
		page = wikipedia.page(title)
	except wikipedia.exceptions.DisambiguationError as e:
		page = e.options[0]
	except wikipedia.exceptions.PageError as e:
		continue

	title = page.title
	try:
		content = page.content
	except AttributeError as e:
		continue

	if isinstance(title, str) and len(content) > min_length:
		print(title)
		file.write(title + "\n")
		i += 1
	if i > number:
		break

file.close()
