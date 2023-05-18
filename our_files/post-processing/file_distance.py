#reads two files and outputs average file distance between them
# files must be in same line format
#author Ben McAuliffe
#May 2023

import Levenshtein

# read both files
with open('answer.txt') as f1:
    lines1 = f1.readlines()
    
with open('best_text1.txt') as f2:
    lines2 = f2.readlines()

total_distance = 0
for i in range(len(lines1)):
    distance = Levenshtein.distance(lines1[i], lines2[i]) #get the line distances
    total_distance += distance

avg_distance = total_distance / len(lines1) #average across all line

percentage = 100 * (1 - avg_distance / len(lines1))


print("Average Levenshtein distance between the two files as a %: ", percentage)

