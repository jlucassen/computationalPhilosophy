import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d as plt3d
import numpy as np
import numpy.random as r
import scipy.stats as s
from scipy.special import comb

def basic(numVars, numPoints, p = 0.05, showBest = False):
    dists = {}
    count = 0
    if showBest:
        best = {0:0, 1:0, 2:0}
    for i in range(0, numVars): #generate data
        dists[i] = r.normal(0,1,numPoints)
    for i in range(0, numVars):
        for j in range (i+1, numVars):
            pearson = s.pearsonr(dists[i], dists[j])
            if pearson[1] < p: #count correlations significant at given p-value, default is p < 0.05
                count += 1
                if showBest and abs(pearson[0]) > best[0]: 
                    best[0] = abs(pearson[0])  #show most impressive correlation
                    best[1] = i
                    best[2] = j
    if showBest and not best[0] == 0:
        plt.scatter(dists[best[1]], dists[best[2]])
        print(s.pearsonr(dists[best[1]], dists[best[2]]))
        plt.show()
    return count

def plotVarEffect(maxVars, points, varStep, repeat = 1, showDerivatives=0, bonferroni = False):
    x = range(2, maxVars, varStep)
    counts = []
    for numVars in x:
        trials = []
        for _ in range(0, repeat):
            if bonferroni:  #if bonferroni correction is turned on,
                trials.append(basic(numVars, points, p=0.05/comb(numVars, 2)))   #test each hypothesis at a/m to get confidence a, where m is # of hypotheses
            else:
                trials.append(basic(numVars, points))  #if bonferroni is off, just test naively at desired significance level
        counts.append(np.mean(trials)) #record significant correlations found
        print(str(int(numVars/maxVars*100))+'%')
    plt.scatter(x, counts)
    plt.xlabel('variables')
    plt.ylabel('false correlations')
    if showDerivatives > 0:
        data = counts
        for i in range(1, showDerivatives + 1):
            deriv = []
            for j in range(0, len(data) - 1):
                deriv.append((data[j+1] - data[j]) / varStep)
            plt.figure()
            plt.scatter(x[:-i], deriv)
            plt.xlabel('variables')
            plt.ylabel('derivative ' + str(i) + ' of correlations')
            plt.ylim(bottom = 0)
            data = deriv
    plt.show()

def plotPointEffect(variables, maxPoints, pointStep, repeat = 1, showDerivatives = 0, bonferroni = False):
    x = range(3, maxPoints, pointStep)
    counts = []
    for numPoints in x:
        trials = []
        for _ in range(0, repeat):
            if bonferroni:  #if bonferroni correction is turned on,
                trials.append(basic(variables, numPoints, p=0.05/comb(variables, 2)))   #test each hypothesis at a/m to get confidence a, where m is # of hypotheses
            else:
                trials.append(basic(variables, numPoints))  #if bonferroni is off, just test naively at desired significance level
        counts.append(np.mean(trials))
        print(str(int(numPoints/maxPoints*100))+'%')
    plt.scatter(x, counts)
    plt.xlabel('points per variable')
    plt.ylabel('correlations')
    plt.ylim(bottom = 0)
    if showDerivatives > 0:
        data = counts
        for i in range(1, showDerivatives + 1):
            deriv = []
            for j in range(0, len(data) - 1):
                deriv.append((data[j+1] - data[j]) / pointStep)
            plt.figure()
            plt.scatter(x[:-i], deriv)
            plt.xlabel('points per variable')
            plt.ylabel('derivative ' + str(i) + ' of correlations')
            data = deriv
    plt.show()

def plotEffect2d(maxVars, maxPoints, varStep, pointStep, bonferroni = False):
    x = range(2, maxPoints, pointStep)
    y = range(3, maxVars, varStep)
    counts = np.zeros((len(y), len(x)))
    for variables in range(0, len(y)):
        for points in range(0, len(x)):
            if bonferroni:  #if bonferroni correction is turned on,
                counts[variables][points] = basic(y[variables], x[points], p=0.05/comb(variables, 2))   #test each hypothesis at a/m to get confidence a, where m is # of hypotheses
            else:
                counts[variables][points] = basic(y[variables], x[points])  #if bonferroni is off, just test naively at desired significance level
        print(str(int(y[variables]/maxVars*100))+'%')
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    X, Y = np.meshgrid(x, y)
    ax.plot_surface(X, Y, counts)
    ax.set_xlabel('data points')
    ax.set_ylabel('variables')
    ax.set_zlabel('correlations found')
    plt.show()


#print(basic(1000, 20, showBest=True))    #basic example. Pretty strong correlations can pop up randomly if you scan enough variables
#plotVarEffect(1000, 10, 100)    #adding variables increases false correlations, superlinear (derivatives?)
#plotVarEffect(200, 10, 20, 100, 2)      #false correlations are roughly quadratic with variables. High derivatives need many trials
#plotPointEffect(20, 200, 10, 100, 1)      #adding more data points has no effect (yeah I did some more research and this makes sense)
#plotEffect2d(500, 200, 50, 20)    #show pointEffect and varEffect  (haha this method is kinda useless now)
#plotVarEffect(200, 10, 2, bonferroni = True)    #with Bonferroni correction, false correlations occur about 1/20 times. p-value correct