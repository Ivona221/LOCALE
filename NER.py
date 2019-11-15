# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 09:57:58 2019

@author: ivona
"""

from cltk.tag import ner

from cltk.stem.latin.j_v import JVReplacer

f = open("latinText.txt", "r", encoding='utf8')
text = f.read()


f1 = open("proper_names.txt", "r", encoding='utf8')
names = f1.read()
namesList = names.split()

f2 = open("entities.txt", "r", encoding='utf8')
entities = f2.read()
entitiesList = entities.split()

f3 = open("people.txt", "r", encoding='utf8')
people = f3.read()
peopleList = people.split()

locations = []

adverbs = ['de', 'in', 'iuxta', 
           'versus', 'apud', 'Datum', 'ad', 'Dat.',
           'vocaturivus', 'dicitur', 'inter', 
           'comes', 'electi']

suffixes = ['ensis', 'ensi', 'ensem', 'enses', 'ense' 'ensium', 'iani', 'ianus', 'anum', 'anorum', 'anarum']

saints = ['sanctam', 'sancti', 'sancto', 'sanctum', 'sanctas', 'sancte', 'sanctus']

i=0

splittedText = text.split(' ')
textSet = set(splittedText)
print(len(textSet))
locationsList = []

print("Starting riles...")
for j in range (0, len(splittedText)):
    word = splittedText[j]
    word = word.strip()
    if word == '':
        continue
    if True:
        # check if the words starts with a capital letter (all the locations start with a capital letter)
        if word[0].isupper() and len(word) > 1 and word[1].isnumeric() == False and word[1].isupper() == False:           
            previousWord = splittedText[j-1].strip()
            nextWord = splittedText[j+1].strip()
            prePrevious = splittedText[j-2].strip()
            prePrePrevious = splittedText[j-3].strip()
            if word.lower() not in adverbs and previousWord != ".":
                if previousWord in adverbs:
                    flag = 0
                    if nextWord[0].isupper():
                        tup = (word + " "+ nextWord, 'LOCATION')                           
                    else:
                        tup = (word, 'LOCATION')
                    locationsList.append(tup)
                    if previousWord == "de":                        
                        if (prePrevious[0].isupper() == False or 
                            ((prePrevious == 'iunioris' or prePrevious == 'senioris' or prePrevious == 'fratrum') 
                            and prePrePrevious[0].isupper() == False)):
                            if nextWord == ',':
                                for k in range(j+2, len(splittedText)):
                                    followingWord = splittedText[k]
                                    if followingWord[0].isupper() and len(followingWord) > 1 and followingWord[1].isnumeric() == False and followingWord[1].isupper() == False:
                                        tup = (followingWord, 'LOCATION')
                                        locationsList.append(tup)
                                    elif followingWord != "," and followingWord != "et":
                                        break
                            elif nextWord == 'et':
                                for k in range(j+2, len(splittedText)):
                                    followingWord = splittedText[k]
                                    if followingWord[0].isupper() and len(followingWord) > 1 and followingWord[1].isnumeric() == False and followingWord[1].isupper() == False:
                                        tup = (followingWord, 'LOCATION')
                                        locationsList.append(tup)
                                    else:
                                        break
                    else:
                        if nextWord == ',':
                                for k in range(j+2, len(splittedText)):
                                    followingWord = splittedText[k]
                                    if followingWord[0].isupper() and len(followingWord) > 1 and followingWord[1].isnumeric() == False and followingWord[1].isupper() == False:
                                        tup = (followingWord, 'LOCATION')
                                        locationsList.append(tup)
                                    elif followingWord != "," and followingWord != "et":
                                        break
                        elif nextWord == 'et':
                            for k in range(j+2, len(splittedText)):
                                followingWord = splittedText[k]
                                if followingWord[0].isupper() and len(followingWord) > 1 and followingWord[1].isnumeric() == False and followingWord[1].isupper() == False:
                                    tup = (followingWord, 'LOCATION')
                                    locationsList.append(tup)
                                else:
                                    break
                elif previousWord in saints:
                    tup = (previousWord + " " + word, 'LOCATION-ENTITIES')
                    locationsList.append(tup)
                elif previousWord in saints and word in entities:
                    tup = (word + " " + nextWord, 'LOCATION-ENTITIES')
                    locationsList.append(tup)
                elif previousWord in peopleList:
                    tup = (word, 'LOCATION-PEOPLE')
                    locationsList.append(tup)
                elif previousWord in entitiesList:
                    if previousWord == 'Ciuitate' or previousWord == 'Ciutatis' or previousWord == 'pontem' or previousWord == "Villam" or previousWord == "Villa" or previousWord == "Forum":                 
                        tup = (previousWord + " " + word, 'LOCATION-ENTITIES')
                    else:
                        tup = (word, 'LOCATION-ENTITIES')
                    locationsList.append(tup)
                    if nextWord == ',':
                        for k in range(j+2, len(splittedText)):
                            followingWord = splittedText[k]
                            if followingWord[0].isupper() and len(followingWord) > 1 and followingWord[1].isnumeric() == False and followingWord[1].isupper() == False:
                                tup = (followingWord, 'LOCATION')
                                locationsList.append(tup)
                            elif followingWord != "," and followingWord != "et":
                                break                        
                elif nextWord in entitiesList:
                    tup = (word, 'LOCATION-ENTITIES')
                    locationsList.append(tup)
                else:
                    for suffix in suffixes:
                        if(word.endswith(suffix)):
                            tup = (word, 'LOCATION')
                            locationsList.append(tup)
                            break


    
fileLocationsCorrect = open("ExtractedLocations.txt", "r");
locationsCorrect = fileLocationsCorrect.read()
locationsCorrectList = locationsCorrect.split('\n')
locationsCorrectLength = len(locationsCorrectList)
#print(locationsCorrectList)

print("False Negatives")
locationsCorrectSet = set(locationsList)
locationsWrong = []
for loc in locationsCorrectSet:
    if loc[0] not in locationsCorrectList:
        locationsWrong.append(loc[0])
        print(loc[0])


locationsListPredicted = []
fWrite = open(" locationPredicted.txt","w+", encoding='utf8')                
for location in locationsList:
    fWrite.write(location[0] + " " + location[1] + "\n")
    if location[0] in locationsCorrectList:
        locationsListPredicted.append(location[0])
    if location[0].replace('u','v') in locationsCorrectList:
        locationsListPredicted.append(location[0].replace('u', 'v'))


locationsPredictedLength = len(locationsListPredicted)

locationsWordByWord = []
locationsListCorrectUnique = list(set(locationsCorrectList))
for l in locationsListCorrectUnique:
    words = l.split()
    for w in words:        
        locationsWordByWord.append(w)
#print(locationsListCorrectUnique)
        
locationsWordByWordLength = len(locationsWordByWord)
print("locations word by word "+ str(locationsWordByWordLength))

locationsPredictedUnique = list(set(locationsListPredicted))

locationsListCorrectUniqueLen = len(locationsListCorrectUnique)
locationsPredictedUniqueLen = len(locationsPredictedUnique)

print("False Positives")
truePredFalse = []
for i in range(0, locationsListCorrectUniqueLen):
    loc = locationsListCorrectUnique[i]
    if loc not in locationsPredictedUnique:
        truePredFalse.append(loc)
        print(loc)

percent = (locationsPredictedUniqueLen/locationsListCorrectUniqueLen)*100
print(percent)
        
                    
                
    
                
                
    
