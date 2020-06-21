import random as r
import statistics as s
import matplotlib.pyplot as plt
import numpy as np

def basicSim(num = 1000, gen = 100, mutProb = 0.05, init = 1): #basic evolution simulator
    history = []
    pop = []
    for _ in range(0, num): #generate initial population
        pop.append(r.random()*init)
    history.append(pop[:])
    for _ in range(0, gen): #main sim loop, iterate over all generations
        for p in pop:
            if r.random() > p: #cull population, depending on survival gene
                pop.remove(p)
        newPop = []
        for _ in range(0, num):
            if r.random() > mutProb: #if no mutation occurs,
                newPop.append(r.choice(pop))  #repopulate randomly from survivors
            else: 
                newPop.append(r.random()) #if mutation does ocurr, generate a new random gene
        pop = newPop #prepare for next cycle
        history.append(pop[:]) #record each generation
    return history

def polySim(num = 1000, gen = 100, mutProb = 0.05, init = 1, weights = [0.1, 0.9]): #simulate multiple genes, with varying survival importance
    history = []
    pop = []
    numGenes = len(weights) #this is how many genes we're simulating
    for _ in range(0, num): 
        individual = []
        for _ in range(0, numGenes): #create individuals as lists, with numGenes random genes
            individual.append(r.random()*init)
        pop.append(individual)
    history.append(pop[:])
    for _ in range(0, gen): #main sim loop
        for p in pop: #cull
            fitness = 0
            for gene in range(0, numGenes):
                fitness += p[gene]*weights[gene] #calculate fitness as weighted sum of genes  (sum or product?)
            if r.random() > fitness: 
                pop.remove(p)
        newPop = []
        for _ in range(0, num): #repopulate
            if r.random() > mutProb: 
                newPop.append(r.choice(pop))
            else: 
                individual = []
                for _ in range(0, numGenes): #create individuals as lists, with numGenes random genes
                    individual.append(r.random())
                newPop.append(individual)
        pop = newPop 
        history.append(pop[:]) #record
    return history

def traitSim(num = 1000, gen = 100, mutProb = 0.05, init = 1):
    history = []
    pop = []
    for _ in range(0, num):
        pop.append([r.random()*init, r.random()*init]) #individuals have 2 genes, survival and trait
    for i in range(0, num):
        pop[i].append(r.random() < pop[i][1]) #create a binary trait, propensity determined by trait gene
    history.append(pop[:])
    for i in range(0, gen): #main sim loop
        for p in pop: #cull based on survival gene
            if r.random() > p[0]: 
                pop.remove(p)
        newPop = []
        for i in range(0, num): #repopulate
            if r.random() > mutProb: 
                newPop.append(r.choice(pop))
            else: 
                individual = [r.random(), r.random()] #create survival and trait genes
                individual.append(r.random() < individual[1]) #determine trait
                newPop.append(individual)
        pop = newPop 
        history.append(pop[:]) #record
    return history

def printSliceMembers(pop):
    for p in pop:
        print(p)

def printSliceSummary(pop, popType = 'basic'):
    if popType == 'basic':
        print("Average survival gene: " + str(s.mean(pop)))
        print("Survival gene variance: " + str(s.variance(pop)))
    if popType == 'poly':
        npPop = np.asarray(pop)
        for i in range(0, len(pop[0])):
            print("Average survival gene " + str(i) + ": " + str(s.mean(npPop[:, i])))
            print("Survival gene " + str(i) + " variance: " + str(s.variance(npPop[:, i])))
    if popType == 'trait':
        yesSurvival = []
        yesTrait = []
        noSurvival = []
        noTrait = []
        for p in pop:
            if p[2]:
                yesSurvival.append(p[0])
                yesTrait.append(p[1])
            else:
                noSurvival.append(p[0])
                noTrait.append(p[1])
        print("Average survival gene with trait: " + str(s.mean(yesSurvival)))
        print("Survival gene variance with trait: " + str(s.variance(yesSurvival)))
        print("Average trait gene with trait: " + str(s.mean(yesTrait)))
        print("Trait gene variance with trait: " + str(s.variance(yesTrait)))
        print("Average survival gene without trait: " + str(s.mean(noSurvival)))
        print("Survival gene variance without trait: " + str(s.variance(noSurvival)))
        print("Average trait gene without trait: " + str(s.mean(noTrait)))
        print("Trait gene variance without trait: " + str(s.variance(noTrait)))

def plotSliceHistogram(pop, popType = 'basic'):
    if popType == 'basic':
        plt.hist(pop)
    if popType == 'poly':
        npPop = np.asarray(pop)
        for i in range(0, len(pop[0])):
            plt.figure(i)
            plt.hist(npPop[:, i])
    if popType == 'trait':
        yesSurvival = []
        yesTrait = []
        noSurvival = []
        noTrait = []
        for p in pop:
            if p[2]:
                yesSurvival.append(p[0])
                yesTrait.append(p[1])
            else:
                noSurvival.append(p[0])
                noTrait.append(p[1])
        plt.figure()
        plt.title('Survival gene with trait')
        plt.hist(yesSurvival)
        plt.figure()
        plt.title('Trait gene with trait')
        plt.hist(yesTrait)
        plt.figure()
        plt.title('Survival gene without trait')
        plt.hist(noSurvival)
        plt.figure()
        plt.title('Trait gene without trait')
        plt.hist(noTrait)
    plt.show()

def plotHistory(history, popType = 'basic', plotVariance = False, label = '', classViews=False):
    if popType == 'basic':
        plt.figure() #plot gene
        plt.title(label + "average survival gene")
        plt.ylim(top=1, bottom=0)  
        for i in range(0, len(history)):
            plt.plot(i, s.mean(history[i]), 'bo')

        if plotVariance:
            plt.figure() #plot variance
            plt.title(label + "survival gene variance")
            plt.ylim(top = 0.1, bottom=0)  
            for i in range(0, len(history)):
                plt.plot(i, s.variance(history[i]), 'ro')

    if popType == 'poly':
        npHistory = np.asarray(history)
        for gene in range(0, len(history[0][0])):
            plt.figure()
            plt.title(label + "average survival gene " + str(gene))
            plt.ylim(top=1, bottom=0)
            for i in range(0, len(history)):
                plt.plot(i, s.mean(npHistory[i, :, gene]), 'bo')

            if plotVariance:
                plt.figure()
                plt.title(label + "survival gene " + str(gene) + " variance")
                plt.ylim(top = 0.1, bottom=0)  
                for i in range(0, len(history)):
                    plt.plot(i, s.variance(npHistory[i, :, gene]), 'ro')

    if popType == 'trait':
        npHistory = np.asarray(history)
        yesSurvival = []
        yesTrait = []
        noSurvival = []
        noTrait = []
        for gen in range(0, len(history)): #iterate through all generations in history
            yesSurvival.append([])
            yesTrait.append([])
            noSurvival.append([])
            noTrait.append([])
            for i in npHistory[gen]: #sort data into trait classes
                if i[2]:
                    yesSurvival[-1].append(i[0])
                    yesTrait[-1].append(i[1])
                else:
                    noSurvival[-1].append(i[0])
                    noTrait[-1].append(i[1])
        plt.figure()
        plt.title(label + "average survival gene")
        plt.ylim(top=1, bottom=0)
        for i in range(0, len(history)):
            plt.plot(i, s.mean(npHistory[i, :, 0]), 'bo')
        if plotVariance:
            plt.figure()
            plt.title(label + "survival gene variance")
            plt.ylim(top=0.1, bottom=0)
            for i in range(0, len(history)):
                plt.plot(i, s.variance(npHistory[i, :, 0]), 'ro')
        plt.figure()
        plt.title(label + "average trait gene")
        plt.ylim(top=1, bottom=0)
        for i in range(0, len(history)):
            plt.plot(i, s.mean(npHistory[i, :, 1]), 'bo')
        if plotVariance:
            plt.figure()
            plt.title(label + "survival trait variance")
            plt.ylim(top=0.1, bottom=0)
            for i in range(0, len(history)):
                plt.plot(i, s.variance(npHistory[i, :, 1]), 'ro')
        if classViews:
            plt.figure()
            plt.title(label + "average survival gene with trait")
            plt.ylim(top=1, bottom=0)
            for i in range(0, len(history)):
                plt.plot(i, s.mean(yesSurvival[i]), 'bo')
            if plotVariance:
                plt.figure()
                plt.title(label + "survival gene variance with trait")
                plt.ylim(top=0.1, bottom=0)
                for i in range(0, len(history)):
                    plt.plot(i, s.variance(yesSurvival[i]), 'ro')
            plt.figure()
            plt.title(label + "average trait gene with trait")
            plt.ylim(top=1, bottom=0)
            for i in range(0, len(history)):
                plt.plot(i, s.mean(yesTrait[i]), 'bo')
            if plotVariance:
                plt.figure()
                plt.title(label + "trait gene variance with trait")
                plt.ylim(top=0.1, bottom=0)
                for i in range(0, len(history)):
                    plt.plot(i, s.variance(yesTrait[i]), 'ro')
            plt.figure()
            plt.title(label + "average survival gene without trait")
            plt.ylim(top=1, bottom=0)
            for i in range(0, len(history)):
                plt.plot(i, s.mean(noSurvival[i]), 'bo')
            if plotVariance:
                plt.figure()
                plt.title(label + "survival gene variance without trait")
                plt.ylim(top=0.1, bottom=0)
                for i in range(0, len(history)):
                    plt.plot(i, s.variance(noSurvival[i]), 'ro')
            plt.figure()
            plt.title(label + "average trait gene without trait")
            plt.ylim(top=1, bottom=0)
            for i in range(0, len(history)):
                plt.plot(i, s.mean(noTrait[i]), 'bo')
            if plotVariance:
                plt.figure()
                plt.title(label + "trait gene variance without trait")
                plt.ylim(top=0.1, bottom=0)
                for i in range(0, len(history)):
                    plt.plot(i, s.variance(noTrait[i]), 'ro')


#plotSliceHistogram(basicSim()[5])  #shows how population tends towards higher genes very quickly
#plotHistory(basicSim(), plotVariance = True, label = 'base case')    #success! 
#plotHistory(basicSim(mutProb=0.2), plotVariance = True, label = 'high mutation')    #effect of mutation rate on equilibrium
#plotHistory(basicSim(init=0.1), plotVariance=True)      #positive selection turns to purifying selection: variability rises, then falls
#plotSliceHistogram(polySim()[5], 'poly')   #demonstrates how more important genes evolve faster
#plotHistory(polySim(gen = 300), 'poly', plotVariance=True)     #gene unimportance has same effects as higher mutation rate! eq point down, variance up
#plotSliceHistogram(traitSim()[5], 'trait')     #trait gene is, of course, higher in population with trait. Does this increase over time?
plotHistory(traitSim(num = 5000, gen=100), 'trait', plotVariance=False)    #nope, just random walk. Makes sense in retrospect
plt.show()

#y dont it have selection effects?