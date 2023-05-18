# attempt 2 at post-processing 
# reads output from the model and tries to convert it into readable words 
#pure edit distance no mods
# Author Ben McAuliffe
# May 2023

import spacy
import Levenshtein
import os #needed if using an env (spacy has weird depencencies)

# Get the home directory
home_dir = os.path.expanduser("~")

# Specify the absolute path to the data folder
data_dir = os.path.join(home_dir, "absolute_path")

# Load the dictionary file
with open(os.path.join(data_dir, "1915-16_words.txt"), "r") as f:
    dictionary = set(f.read().split())

with open(os.path.join(data_dir, "output.txt"), "r") as f:
    lines = f.readlines()   

#spaCy setting
nlp = spacy.load('en_core_web_sm')

corrected_lines = []
for line in lines:
    doc = nlp(line) #convert line in to an nlp object (includes parts of speech)
    corrected_words = []
    for token in doc:
        if token.is_alpha and token.text not in dictionary:
            closest_word = min(dictionary, key=lambda x: Levenshtein.distance(token.text, x)) #finds the closest edit dist word in the disctionary
            # Filter out suggestions that have different parts of speech
            # if token.pos_ == nlp(closest_word)[0].pos_: # made things worse, in futre check the previous word instead
            # of the line at the begining because spaCy is best with correctly spelled words
            #     corrected_words.append(closest_word)
            # else:
            #     corrected_words.append(token.text)
            corrected_words.append(closest_word)

        else:
            corrected_words.append(token.text)
    corrected_line = ' '.join(corrected_words)
    corrected_lines.append(corrected_line)

corrected_text = '\n'.join(corrected_lines)

#output file name
with open('corrected_text7.txt', 'w') as f:
    f.write(corrected_text)

