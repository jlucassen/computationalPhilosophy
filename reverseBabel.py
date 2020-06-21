import numpy as np
import matplotlib.pyplot as plt
import statistics as st

#np.random.seed(1738)

alphabet = {}  #Frequency distribution of letters doesn't seem to fit any clean curve, used empirical data instead.
alphabet['e'] = 0.12702 
alphabet['t'] = 0.09056
alphabet['a'] = 0.08167
alphabet['o'] = 0.07507
alphabet['i'] = 0.06966
alphabet['n'] = 0.06749
alphabet['s'] = 0.06327
alphabet['h'] = 0.06094
alphabet['r'] = 0.05987
alphabet['d'] = 0.04253
alphabet['l'] = 0.04025
alphabet['c'] = 0.02782
alphabet['u'] = 0.02754
alphabet['m'] = 0.02406
alphabet['w'] = 0.02360
alphabet['f'] = 0.02228
alphabet['g'] = 0.02015
alphabet['y'] = 0.01974
alphabet['p'] = 0.01929
alphabet['b'] = 0.01492
alphabet['v'] = 0.00978
alphabet['k'] = 0.00772
alphabet['j'] = 0.00153
alphabet['x'] = 0.00150
alphabet['q'] = 0.00095
alphabet['z'] = 0.00074

def generateCorpus(alph = alphabet, spaceProb0 = 0.2, spaceProbScale = 1.1, corpusSize = 50000): #Generates a corpus of words, each associated with a frequency
    corpus = {}
    while len(corpus) < corpusSize: #continues until generated corpusSize distinct words
        newWord = ''
        terminate = False
        spaceProb = spaceProb0
        while not terminate: #loop until word is terminated
            choice = np.random.random() #random number 0-1
            for letter in alph: #select letter according to probabilities. There's likely a better way to do this, but this works.
                choice -= alph[letter]
                if choice <= 0:
                    newWord += letter
                    break
            if np.random.random() < spaceProb: #check if word will be terminated
                terminate = True
            spaceProb *= spaceProbScale #if word is not terminated, increase termination probability
        if not newWord in corpus.keys():
            corpus[newWord] = 1 #If word is new, add to dictionary
        else:
            corpus[newWord] += 1 #if word is not new, update frequency
    return corpus

def plotCorpus(corpus):
    wordLengths = list(map(len, corpus.keys())) #list of all word lengths
    zipf = sorted(corpus.values(), reverse = True) #sorted list of frequencies, in descending order
    print(st.mean(wordLengths)) #output mean word length, without weighting for usage
    plt.figure(1)
    plt.hist(wordLengths, np.arange(0, 15, 1), density = True) #plots word length distribution, not usage-weighted
    plt.title('Word Length Probability Density Histogram')
    plt.xlabel('Word length')
    plt.ylabel('Probability density')
    plt.figure(2)
    plt.loglog(zipf) #plots usages of words, to check if result is Zipf-y like real language
    plt.title('Zipf Distribution, Log Domain')
    plt.xlabel('Log Word Usage Rank')
    plt.ylabel('Log Word Usage Count')
    plt.figure(3)
    plt.scatter(range(0, 50), zipf[0:50]) #plots usages of words in log, to confirm Zipf-iness
    plt.title('Zipf Distribution, Linear Domain')
    plt.xlabel('Word Usage Rank')
    plt.ylabel('Word Usage Count')
    plt.show()

def generateSentence(corpus, averageLength = 15):
    total = sum(corpus.values()) #add up all word frequencies
    out = []
    length = np.random.poisson(averageLength) #Average sentence length is ~15, roughly poisson distribution
    for i in range(0, length):
        choice = int(np.random.random(1)[0] * (total+1)) #generate number from 0-total
        for word in corpus: #choose word according to probabilities. Again, likely a better way to do this.
            choice -= corpus[word]
            if choice <= 0:
                out.append(word) #add to sentence list
                break
    return out

def simExchange(num = 10000):
    c1 = generateCorpus() #speaker's corpus
    c2 = generateCorpus() #listener's corpus
    count = 0
    for _ in range(0, num):
        success = True #nothing has gone wrong yet
        s = generateSentence(c1) #speak a sentence
        for word in s:
            if not word in c2.keys(): #Check if listener recognizes all words
                success = False #If something went wrong, end sentence to save time
                break
        if success: #IF nothing went wrong, Borges emerges triumphant
            count += 1
    return count #output number of successfully disguised miscommunications

def printSentence(sentenceArray):
    strSentence = ' '.join(sentenceArray)+ '.'
    capFirst = strSentence[0].upper() + strSentence[1:]
    print(capFirst)