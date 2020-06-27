import requests
import json
import string

#To-do:
#use full definitions instead of shortdef
#visualize somehow
#bypass API if needed, just parse the HTML

def findIsland():
    print("Enter api key:")     #get ur own key bub
    key = input()
    print("Enter root word:")   #choose word to build island around
    root = input()
    island = []     #initialize island: words whose connections have been fully explored
    shore = [root]      #initialize shore: words whose connections are next to be explored
    apiCalls = 0    #count api calls in this session. Max daily allowed is 1000 :(
    while len(shore) > 0:
        sea = []    #initialize sea: new words found by exploring shore connections
        for word in shore:
            raw = requests.get("https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + word + "?key=" + key).text
            apiCalls += 1
            data = json.loads(raw)
            if len(data) == 0:  #if  a word is so badly misspelled that there are no suggestions,
                print("Word not recognized. No suggustions available, wow")
                if len(shore) > 1:
                    continue
                else:
                    quit()
            elif isinstance(data[0], str):   #if a word isn't in the dictionary, api passes back a list containing strings suggesting corrections
                print("Word not recognized. Did you mean: " + str(data) + "?")
                if len(shore) > 1:
                    continue
                else:
                    quit()
            elif not isinstance(data[0], dict):    #if word is recognized, list will contain a dict. If it doesn't, something's funky
                print("uhh idk what happened bud, something ain't right.")
                quit()
            elif len(data[0]['shortdef']) > 0:   #if all goes well, 
                for shortdef in [data[0]['shortdef'][0]]:      #lol
                    defWordList = shortdef.split()     #break up into words
                    for defWord in defWordList:
                        if not (defWord in island or defWord in shore or defWord in string.punctuation):
                            sea.append(defWord)     #add approved words to sea
        island = island + shore    #add explored words to island
        shore = sea     #move new words to shore
        print(str(len(island)) + " words fully explored. " + str(len(shore)) + " words to explore next. So far, made " + str(apiCalls) + " api calls this session. Continue? y/n")
        if not input() == 'y':      #if user says anything other than yes, stop. Proper consent baybee
            quit()
    print('Island needs ' + len(island) + 'words to be complete, and cut off from rest of dictionary')

findIsland()        #all the islands are too big :(