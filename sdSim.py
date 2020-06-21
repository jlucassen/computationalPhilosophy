import matplotlib.pyplot as plt

dP = { #keep default parameters for different simulations all in the same place
'S0':99999000, #population of 100M
'E0':0, #none exposed initially
'I0':1000, #1000 initial infected
'R0':0, #none recovered initially
'D0':0, #no deaths initially
'ic':0.2, #5-day incubation period
'cc0':0.14, #cc0 calculated by cc0 = R0*rc. Infections/(person*day) = (total infections/person)*(1/days infectious). Used ballpark of r0 of 2
'rc':0.07, #14-day recovery time
'dc0':0.05, #5% base fatality rate for infected
'medCap': 100000, #100K medical capacity before fatalities increase
'medRate': 0.05, #5% hospitalization rate
'sd': 10,  #max social distancing factor of 10
'lag': 0, #lag on social distanding policy action, in days.By default, don't include
't':730, #simulate 2 years
'step':1 #by default, adjust distancing every day, AKA continuously
}

def SEIR(S0=dP['S0'], E0=dP['E0'], I0=dP['I0'], R0=dP['R0'], ic=dP['ic'], cc0=dP['cc0'], rc=dP['rc'], t=dP['t']): #basic SEIR model
    #S = suceptible (uninfected), E = exposed (incubation), I = infectious, R = recovered. Order of magnitude set to US population
    #ic = incubation coefficient, or 1 / (avg incubation period). Usually called alpha or a
    #cc = contact coefficient, or (number of daily contacts per person) / (total population). Usually called beta or b
    #rc = recovery coefficient, or 1 / (avg recovery time). Usually called gamma or c    

    cc = cc0 / (S0 + E0 + I0 + R0) #actual factor cc has to be divided by total pop. cc*I = number of contacts made by infectious, and S/pop is propoportion of those contact that will be with suceptible individuals

    S = [S0]
    E = [E0]
    I = [I0]
    R = [R0]
    for _ in range(0, t):
        dS = -cc*S[-1]*I[-1] #change in suceptible = - number of contacts between suceptible and infectious
        dE = cc*S[-1]*I[-1] - ic*E[-1] #change in exposed = new exposed by contact between S and I - number of exposed that become infectious
        dI = ic*E[-1] - rc*I[-1] #change in infectious = number of exposed that become infectious - number of infectious that recover
        dR = rc*I[-1] #change in recovered = number of infectious that recover

        S.append(S[-1] + dS)
        E.append(E[-1] + dE)
        I.append(I[-1] + dI)
        R.append(R[-1] + dR)
    return {'S':S, 'E':E, 'I':I, 'R':R}

def SEIRD(S0=dP['S0'], E0=dP['E0'], I0=dP['I0'], R0=dP['R0'], D0=dP['D0'], ic=dP['ic'], cc0=dP['cc0'], rc=dP['rc'], dc0=dP['dc0'], medCap=dP['medCap'], medRate=dP['medRate'], t=dP['t']): #SEIR model with D category added to track deaths
    #dc0 = base death coefficient, or % of infected that will die rather than recovering if treated
    #medCap = medical capacity, if any more are infected ata a time fatalities double. Order of magnitude set to match US
    
    cc = cc0 / (S0 + E0 + I0 + R0) 
    dc = dc0
    if I0 >= medCap:
        dc = dc0 * 2

    S = [S0]
    E = [E0]
    I = [I0]
    R = [R0] #R now no longer includes deaths
    D = [D0] #D tracks deaths
    
    for _ in range(0, t):
        if I[-1]*medRate >= medCap:
            dc = dc0 * 2

        dS = -cc*S[-1]*I[-1]
        dE = cc*S[-1]*I[-1] - ic*E[-1]
        dI = ic*E[-1] - rc*I[-1]
        dR = rc*(1-dc)*I[-1] #dR is now those that recover and do not die (1-dc)
        dD = rc*dc*I[-1] #change in deaths = number of people that recover * mortality rate (dc)

        S.append(S[-1] + dS)
        E.append(E[-1] + dE)
        I.append(I[-1] + dI)
        R.append(R[-1] + dR) 
        D.append(D[-1] + dD) 
    return {'S':S, 'E':E, 'I':I, 'R':R, 'D':D}

def SEIRD_sd(S0=dP['S0'], E0=dP['E0'], I0=dP['I0'], R0=dP['R0'], D0=dP['D0'], ic=dP['ic'], cc0=dP['cc0'], rc=dP['rc'], dc0=dP['dc0'], medCap=dP['medCap'], medRate=dP['medRate'], sd=dP['sd'], lag=dP['lag'], step=dP['step'], t=dP['t']): #SEIRD with social distancing proportional to infected population
    #sd represents maximum social distancing factor: if population 100% infected, social contact reduced by a factor of sd

    P = (S0 + E0 + I0 + R0) #calculate total population, to avoid recalculating all the time
    if lag > 0:
        sdc = 1 #because of lag, no social distancing initially, coefficient = 1
    else:
        sdc = 1/(((sd-1)*I0/P)+1) #if population is 100% infected, social distancing coefficient is 1/sd. If 0% infected, sdc = 1. Division factor increases linearly w % infected
    cc = cc0 / (S0 + E0 + I0 + R0) 
    dc = dc0
    if I0 >= medCap:
        dc = dc0 * 2

    S = [S0]
    E = [E0]
    I = [I0]
    R = [R0] 
    D = [D0] 
    for day in range(0, t):
        if day >= lag: #once initial lag period has ended
            if day%step== 0: #if today is a decision day
                sdc = 1/(((sd-1)*I[-1-lag]/P)+1) #adjust social distancing policy
        if I[-1]*medRate >= medCap: #model as if 5% of cases require hospitalization
            dc = dc0 * 2

        dS = -cc*sdc*S[-1]*I[-1] #new infections now multiplied by sdc
        dE = cc*sdc*S[-1]*I[-1] - ic*E[-1] #new infections now multiplied by sdc
        dI = ic*E[-1] - rc*I[-1]
        dR = rc*(1-dc)*I[-1] 
        dD = rc*dc*I[-1] 

        S.append(S[-1] + dS)
        E.append(E[-1] + dE)
        I.append(I[-1] + dI)
        R.append(R[-1] + dR) 
        D.append(D[-1] + dD) 
    return {'S':S, 'E':E, 'I':I, 'R':R, 'D':D}

def plotOne(data, logMode=False): #Plots one simulation from a dictionary of lists containing data for each variable and keyed with variable names
    for varName in data.keys():
        plt.plot(data[varName], label = varName) #plots each variable - data stored in list keyed by name
    plt.legend()
    plt.xlabel = "Time (days)"
    plt.ylabel = "Count (people)"
    if logMode:
            plt.yscale('log')
    plt.show()

def plotMulti(data, logMode=False): #Plots multiple simulations together for comparison
    for i in range(0, len(data)):
        plt.figure(i)
        for varName in data[i].keys():
            plt.plot(data[i][varName], label = varName)
        plt.legend()
        plt.title = "Figure " + str(i)
        plt.xlabel = "Time (days)"
        plt.ylabel = "Count (people)"
        if logMode:
            plt.yscale('log')
    plt.show()

def multiSim(function, pValues, logMode=False): #examine how different values of a certain parameter impact a function
    data = []
    for kwargs in pValues:
        data.append(function(**kwargs)) #Passes arguments for each case in as a dictionary, with values identified by parameter names.
    plotMulti(data, logMode) #returns results as a list of dicts, ready for plotMulti

#plotOne(SEIRD())
#plotMulti([SEIRD_sd(), SEIRD_sd(lag=10), SEIRD_sd(lag=20), SEIRD_sd(lag=30), SEIRD_sd(lag=40)])
multiSim(SEIRD_sd, [{'step':60, 'lag':60, 'sd':10}, {'step':60, 'lag':60, 'sd':20}, {'step':60, 'lag':60, 'sd':30}])
