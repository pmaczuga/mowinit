import numpy as np
import wikipedia
import string

filename = "Pages titles.txt"
num_of_pages = 10

num_of_words = dict()
dictionary = dict()
titles = list()
contents = list()
vectors = list()

def fill_num_of_words(file):
    for i in range(num_of_pages):
        title = file.readline()
        titles.append(title)
        try:
            page = wikipedia.page(title)
        except wikipedia.exceptions.DisambiguationError as e:
            page = e.options[0]
        print("Processing: ",  title)

        contents.append(page.content.strip(string.punctuation).split(" "))
        for word in contents[-1]:
            num_of_words[word] = num_of_words.setdefault(word, 0) + 1

def fill_dictionary():
    i = 0
    length = len(num_of_words)
    print("Number of words: ", length)
    for word in num_of_words.keys():
        vector_as_list = [0 for j in range(length)]
        vector_as_list[i] = 1
        dictionary[word] = tuple(vector_as_list)
        i += 1

def fill_titles_and_contents():
    pass

def main():
    wikipedia.set_lang("en")
    file = open(filename, "r")

    fill_num_of_words(file)


    file.close()

if __name__ == "__main__":
    main()