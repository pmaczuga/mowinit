import numpy as np
np.set_printoptions(threshold=np.inf)
import wikipedia
import string
import re

filename = "Pages titles.txt"
num_of_pages = 3

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

        contents.append(re.sub('['+string.punctuation+']', '', page.content).split())
        for word in contents[-1]:
            num_of_words[word] = num_of_words.setdefault(word, 0) + 1

def fill_dictionary():
    i = 0
    length = len(num_of_words)
    print("Number of words: ", length)
    for word in num_of_words.keys():
        vector = np.zeros(length, dtype=np.int)
        vector[i] = 1
        dictionary[word] = vector
        i += 1

def fill_vectores(file):
    length = len(dictionary)
    for title, content in zip(titles,contents):
        print("To vector: ", title)
        vector = np.zeros(length, dtype=np.int)
        for word in content:
            vector += dictionary[word]
        vectors.append(vector)
        

def main():
    wikipedia.set_lang("en")
    file = open(filename, "r")

    fill_num_of_words(file)
    fill_dictionary()
    fill_vectores(file)

    print(contents[0])
    print(vectors[0])


    file.close()

if __name__ == "__main__":
    main()