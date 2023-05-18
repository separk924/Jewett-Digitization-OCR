#Reads though the transcriptions of the diaries plus dictionary
#of bird and mammal names to create a master dictionary
#author Ben McAuliffe
#April 2023

from pathlib import Path

#open file
file = open('field_diary_1916.txt', mode = 'r', encoding = 'utf-8-sig')
lines = file.readlines()
file.close()
punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~''' #get rid of punctuation as preprocessing go rid of most of it
setOfWords = set() #no dupes
for line in lines:
    for word in line.split():
        for elem in punc:
            for char in word:
                if char == elem:

                    word = word.replace(char, "")
        setOfWords.add(word)
#add some punctuation
setOfWords.add(',')
setOfWords.add('.')
setOfWords.add('-')

#do it all again with next text file

file = open('1915Diary.txt', mode = 'r', encoding = 'utf-8-sig')
lines = file.readlines()
file.close()
punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
for line in lines:
    for word in line.split():
        for elem in punc:
            for char in word:
                if char == elem:

                    word = word.replace(char, "")
        setOfWords.add(word)

#thrid time

file = open('bird&mammalNames.txt', mode = 'r', encoding = 'utf-8-sig')
lines = file.readlines()
file.close()
punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
for line in lines:
    for word in line.split():
        for elem in punc:
            for char in word:
                if char == elem:

                    word = word.replace(char, "")
        setOfWords.add(word)

listOfWords = list(setOfWords)
listOfWords.sort()



#write words into a new file
f = open('1915-16_words.txt', mode = 'w', encoding = 'utf-8-sig')
for word in listOfWords:
    f.write(word + '\n')

f.close()