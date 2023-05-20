# attempt 3 at post-processing 
# reads output from the model and tries to convert it into readable words 
# edit distance with emphasis on the first letter
# Author Ben McAuliffe
# May 2023

import spacy
import Levenshtein
import os


def distance_with_penalty(a, b):
    """
    Computes the Levenshtein distance between two words, with a penalty for shorter words.
    """
    penalty = 0.1  # Penalty factor for longer words
    if a[0] == b[0]:
        distance = Levenshtein.distance(a, b) - 1
    else:
        distance = Levenshtein.distance(a, b)
    penalty_term = penalty * abs(len(b) - len(a))
    return distance + penalty_term

# Get the home directory
home_dir = os.path.expanduser("~")

# Specify the absolute path to the data folder 
data_dir = os.path.join(home_dir, "absolute_path")

# Load the text file
with open(os.path.join(data_dir, "1915-16_words.txt"), "r") as f:
    dictionary = set(f.read().split())

with open(os.path.join(data_dir, "output.txt"), "r") as f:
    lines = f.readlines()   

#spaCy setting
nlp = spacy.load('en_core_web_sm')


corrected_lines = []
for line in lines:
    line.lower()
    doc = nlp(line)
    corrected_words = []
    for token in doc:
        if token.is_alpha and token.text not in dictionary:
            closest_word = min(dictionary, key=lambda x: distance_with_penalty(token.text, x)) #finds the closest dist word in the disctionary
            corrected_words.append(closest_word)

        else:
            corrected_words.append(token.text)
    corrected_line = ' '.join(corrected_words)
    corrected_lines.append(corrected_line)

corrected_text = '\n'.join(corrected_lines)

#write a new file with the text
with open('corrected_text.txt', 'w') as f:
    f.write(corrected_text)


#try now to favor words that have same number on letters or more
#have the words include numbers