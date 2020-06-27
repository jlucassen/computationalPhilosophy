from vpython import *
from random import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def move(x, y, z, r, s, b):
    dx = s * (y - x)
    dy = x * (r - z) - y
    dz = (x * y) - (b * z)

    return([dx, dy, dz])

def singleSim(x, y, z, r, s, b, t, dt, field = False, frameRate = 100):
    canvas(height = 600, width = 1.618*600, align = 'left')
    state = sphere(pos = vec(x,y,z), radius = 0.5, make_trail = True)

    if not field == False:  #if field param is changed from default,
        mapField(r, s, b, **field)  #draw field with given parameters
        scene.waitfor("draw_complete")
        scene.waitfor("draw_complete")

    for _ in arange(0, t, dt): #sim loop
        rate(frameRate) #set frame rate
        step = move(state.pos.x, state.pos.y, state.pos.z, r, s, b)
        state.pos.x += step[0] * dt
        state.pos.y += step[1] * dt
        state.pos.z += step[2] * dt

def multiSim(starts, r, s, b, t, dt, field = False, frameRate = 100):
    canvas(height = 600, width = 1.618*600, align = 'left')
    states = []
    for start in starts:    #initialize starting states
        states.append(sphere(pos = vec(start[0], start[1], start[2]), radius = 0.5, make_trail = True, color = vec(random(), random(), random())))
    
    if not field == False:  #if field param is changed from default,
            mapField(r, s, b, **field)  #draw field with given parameters
            scene.waitfor("draw_complete")
            scene.waitfor("draw_complete")

    for time in arange(0, t, dt): #sim loop
        for state in states: #iterate through each state in parallel
            rate(frameRate) #set frame rate
            step = move(state.pos.x, state.pos.y, state.pos.z, r, s, b)
            state.pos.x += step[0] * dt
            state.pos.y += step[1] * dt
            state.pos.z += step[2] * dt

def mapField(r, s, b, zone = 10, spacing = 1, showColors = True, showArrows = True, unit = True, scale = 1, center = [0, 0, 0]):
    for x in range(center[0]-zone,center[0]+zone+1, spacing):
        for y in range(center[1]-zone,center[1]+zone+1, spacing):
            for z in range(center[2]-zone,center[2]+zone+1, spacing):
                d = move(x, y, z, r, s, b)  #find vector at given location
                dvp = vec(d[0], d[1], d[2])     #convert to vpython vector
                dhat = vec(d[0], d[1], d[2]).hat    #find unit vector
                if showColors:
                    dcolor = dhat * 0.5 + vec(0.5, 0.5, 0.5)    #if color is turned on, code direction into color
                else:
                    dcolor = color.white    #if color turned off, default to white
                if showArrows:
                    if unit:
                        arrow(pos = vec(x, y, z), axis = dhat * scale, color = dcolor)
                    else: 
                        arrow(pos = vec(x, y, z), axis = dvp * scale, color = dcolor)
                else:
                    sphere(pos = vec(x, y, z), radius = spacing / 4 * scale, color = dcolor)  #if arrow turned off, just show small spheres

def trackError(s1, s2, r, s, b, t, dt):
    state1 = s1
    state2 = s2
    history = [sqrt((s1[0]-s2[0])**2 + (s1[1]-s2[1])**2 + (s1[2]-s2[2])**2)]
    for _ in arange(0, t, dt):
        step1 = move(state1[0], state1[1], state1[2], r, s, b)
        step2 = move(state2[0], state2[1], state2[2], r, s, b)
        state1 = [state1[0] + step1[0]*dt, state1[1] + step1[1]*dt, state1[2] + step1[2]*dt]
        state2 = [state2[0] + step2[0]*dt, state2[1] + step2[1]*dt, state2[2] + step2[2]*dt]
        history.append(sqrt((state1[0]-state2[0])**2 + (state1[1]-state2[1])**2 + (state1[2]-state2[2])**2))
    return(history)
    
def errorExplosion(r, s, b, t, dt):
    anchor = [20*random()-10, 20*random()-10, 20*random()-10]
    plt.plot(trackError(anchor, [anchor[0]+random()*0.01, anchor[1]+random()*0.01, anchor[2]+random()*0.01], r, s, b, t, dt))
    plt.plot(trackError(anchor, [anchor[0]+random()*0.00001, anchor[1]+random()*0.00001, anchor[2]+random()*0.00001], r, s, b, t, dt))
    plt.plot(trackError(anchor, [anchor[0]+random()*0.00000001, anchor[1]+random()*0.00000001, anchor[2]+random()*0.00000001], r, s, b, t, dt))

def paramPlaneStability(s1, s2, r, t, dt, zone, threshold):
    heatmap = np.empty((2*zone, 2*zone))
    for s in range(-zone, zone):
        for b in range(-zone, zone):
            state1 = s1
            state2 = s2
            heatmap[s+zone][b+zone] = log(t)
            for time in arange(0, t, dt):
                step1 = move(state1[0], state1[1], state1[2], r, s, b)
                step2 = move(state2[0], state2[1], state2[2], r, s, b)
                state1 = [state1[0] + step1[0]*dt, state1[1] + step1[1]*dt, state1[2] + step1[2]*dt]
                state2 = [state2[0] + step2[0]*dt, state2[1] + step2[1]*dt, state2[2] + step2[2]*dt]
                if sqrt((state1[0]-state2[0])**2 + (state1[1]-state2[1])**2 + (state1[2]-state2[2])**2) > threshold:
                    heatmap[s+zone][b+zone] = log(time)
                    break
            
    im = plt.imshow(heatmap)
    plt.colorbar(im)
    plt.ylabel('sigma (+ range)')
    plt.xlabel('beta (+ range)')
    
def spatialPlaneStability(z, r, s, b, t, dt, zone, threshold):
    heatmap = np.empty((2*zone, 2*zone))
    for x in range(-zone, zone):
        for y in range(-zone, zone):
            state1 = [x,y,z]
            state2 = [x+0.001, y+0.001, z+0.001]
            heatmap[y+zone][x+zone] = log(t)
            for time in arange(0, t, dt):
                step1 = move(state1[0], state1[1], state1[2], r, s, b)
                step2 = move(state2[0], state2[1], state2[2], r, s, b)
                state1 = [state1[0] + step1[0]*dt, state1[1] + step1[1]*dt, state1[2] + step1[2]*dt]
                state2 = [state2[0] + step2[0]*dt, state2[1] + step2[1]*dt, state2[2] + step2[2]*dt]
                if sqrt((state1[0]-state2[0])**2 + (state1[1]-state2[1])**2 + (state1[2]-state2[2])**2) > threshold:
                    heatmap[y+zone][x+zone] = log(time)
                    break
    im = plt.imshow(heatmap)
    plt.colorbar(im)
    plt.ylabel('y (+ range)') 
    plt.xlabel('x (+ range)')

def spatialPlaneFractal(z, r, s, b, t, dt, zone, spacing=1, center = [0,0]):
    coords = np.empty((int(2*zone/spacing), int(2*zone/spacing)), dtype = object)
    xmax = xmin = ymax = ymin = zmax = zmin = 0
    for x, y in np.ndindex(coords.shape):
        state = [x*spacing - zone + center[0],y*spacing - zone + center[0],z*spacing - zone]
        #print(state)
        for _ in arange(0, t, dt):
            step = move(state[0], state[1], state[2], r, s, b)
            state = [state[0] + step[0]*dt, state[1] + step[1]*dt, state[2] + step[2]*dt]
        coords[x][y] = state
        if state[0] > xmax:
            xmax = state[0]
        if state[0] < xmin:
            xmin = state[0]
        if state[1] > ymax:
            ymax = state[1]
        if state[1] < ymin:
            ymin = state[1]
        if state[2] > zmax:
            zmax = state[2]
        if state[2] < zmin:
            zmin = state[2]
    colors = np.empty((int(2*zone/spacing), int(2*zone/spacing), 3))
    for x, y in np.ndindex(coords.shape):
        colors[x][y] = [(coords[x][y][0]-xmin)/(xmax-xmin), (coords[x][y][1]-ymin)/(ymax-ymin), (coords[x][y][2]-zmin)/(zmax-zmin)]
    im = plt.imshow(colors)
            


#singleSim(1, 0, 0, 28, 10, 8/3, 100, 0.001)     #nice! looks like the Lorenz butterfly thing to me
#multiSim([[1,0,0], [-1,0,0], [0,1,0], [0,-1,0]], 28, 10, 8/3, 100, 0.001)      #draw me a butterfly. 180 degree rotational sym about z axis, I wonder what states exactly on the z axis do?
#multiSim([[1,0,0],[100,0,0], [0,100,0], [0,0,100]], 28, 10, 8.0/3.0, 100, 0.001)    #distant states eventually end up in the butterfly (z stays on z axis, approaches origin)

#mapField(28, 10, 8/3)  #that's kinda sick
#mapField(28, 10, 8/3, 1000, 100, unit=False, scale = 0.0005) #from here on, increasing zone, spacing, and scale by the same factor yields pretty much identical results. Unclear whether all flow lines lead to butterfly
#mapField(28, 10, 8/3, 100, 10, unit=False, scale = 0.005) #asymmetry in z-direction clearly visible below this scale
#multiSim([[10,10,0], [-10,0,10]], 28, 10, 8/3, 100, 0.001, field = {'unit':False, 'scale':0.005, 'zone':40, 'spacing':8, 'center':[0,0,30]})  #sanity check - states do appear to change along flow lines

#plt.plot(trackError([1,0,0], [1.01,0,0], 28, 10, 8/3, 50, 0.001))    #1% error stays stable for a while, but then suddenly explodes!
#plt.plot(trackError([1,0,0], [1.00001,0,0], 28, 10, 8/3, 50, 0.001))  #1000x decrease in error staves off explosion for 10,000 dt's
#plt.plot(trackError([1,0,0], [1.00000001,0,0], 28, 10, 8/3, 50, 0.001))   #further 1000x decrease buys almost exactly another 10,000 dt's! Precision needed increases exponentially with time horizon of prediction
#errorExplosion(28, 10, 8/3, 50, 0.001)     #not as clean as the case above, but in general there tends to be a period of accuracy, and then an explosion that can only be slightly pushed out by decreasing error. Not always neatly linear tho

#paramPlaneStability([1,0,0], [1.001,0,0], 28, 100, 0.001, 20, 10)   #the 28,10,8/3 configuration falls within the green peninsula. Maybe other green spaces are similar? Most seem to either explode immediately or stabilize. There's that ridge line too...
#singleSim(1,0,0,28,-1,0,100,0.001)  #huh, this ridge configuration doesn't look anything like the 28,10,8/3 configuration. Kinda resembles how the extreme y start behaved, but spiraling to +z instead of -z, and stable size instead of constricting.
#plt.plot(trackError([1,0,0], [1.001,0,0], 28, -1, 0, 35, 0.001))    #this ridge area is super weird! Seems very orderly, oscillating for a long time, and then suddenly blows up! that's wack
#mapField(28, -1, 0) #movement is dominated by x coordinate, y has little effect, z appears to have almost no effect. Makes sense, based on eq's
#plt.plot(trackError([1,0,0], [1.001,0,0], 28, 15, 3, 50, 0.001))    #peninsula behaves about right, takes about 21,000 cycles to explode, so t = 2100, log(t) = 2.3
#singleSim(1,0,0,28,15,3,100,0.001)  #it's butterfly shaped!
#plt.plot(trackError([1,0,0], [1.001,0,0], 28, 15, 4, 50, 0.001))    #right next door, in the yellow, states converge rather than diverging. 
#singleSim(1,0,0,28,15,4,100,0.001)  #at b=4, in the yellow, the "centers" become traps
#plt.plot(trackError([1,0,0], [1.001,0,0], 28, -5, -5, 1.5, 0.001))  #yeah so in the purple, it explodes real quick
#singleSim(1,0,0,28,-5,-5,100,0.001)     #yikes
#paramPlaneStability([10,10,10], [10.01,10,10], 28, 100, 0.001, 10, 10)    #looks very similar with a different starting point!
#paramPlaneStability([1,0,0], [1.001,0,0], 13, 100, 0.001, 10, 10)   #peninsula gets smaller down to r=14, appears to disappear at r=13. Threshold between explosion and trap stays largely stationary, interestingly
#paramPlaneStability([1,0,0], [1.001,0,0], 65, 100, 0.001, 10, 10)   #a hole in the peninsula!
#singleSim(1,0,0,28,5,2,100,0.001)      #nope, not a true trap - states still spiral out, not in. Likely just highly stable, and bumping into the t=100 cap on the sim.
#paramPlaneStability([1,0,0], [1.001,0,0], 65, 100, 0.001, 10, 10)   #^confirmed. Peninsula shows no real signs of disappearing within a range I can reasonably simulate on my laptop, will probably continue to grow like this into very high sigma, very long time to explosion

#spatialPlaneStability(9, 28, 10, 8/3, 100, 0.001, 10, 10)
#spatialPlaneStability(10, 28, 10, 8/3, 100, 0.001, 10, 10)  #tendency to diverge seems largely confined to the z-axis, with this diagonal bit at z=10
#spatialPlaneStability(11, 28, 10, 8/3, 100, 0.001, 10, 10)

#spatialPlaneFractal(0, 28, 10, 8/3, 1, 0.001, 10, spacing = 0.25)  #makes sense - states divide into two groups almost immediately with 180 degree symmetry. Groups stick together, or even converge somewhat. Border has some random colors, states that go in other directions - supports obs. above
#spatialPlaneFractal(40, 28, 10, 8/3, 1, 0.001, 10, spacing = 0.25)  #did the dividing line rotate a bit?
#spatialPlaneFractal(-40, 28, 10, 8/3, 1, 0.001, 10, spacing = 0.25)     #dividing line appears to corkscrew in the +z direction.
#spatialPlaneFractal(0, 28, 10, 8/3, 4, 0.001, 10, spacing = 0.25)       #whoa that's sick! highly patterned, still symmetric, and more of those those high-divergence bands show up
#spatialPlaneFractal(0, 28, 10, 8/3, 6, 0.001, 10, spacing = 0.25)       #becomes "rougher" with increasing time, bands that stick together get narrower and narrower
#spatialPlaneFractal(0, 28, 10, 8/3, 6, 0.001, 10, spacing = 0.025)        #when zoomed in though, everything is still continuous. I guess this is what a gradual transition from continuity to discontinuity looks like: slope of partials crossing between bands approaches infinity as t goes to infinity
#Importantly - if this is in fact a sort of fractal, as it is clearly patterned, that means that some measurements are more important than others for predicting chaotic systems, and with this method we can find out which. If the bands run horizontally, the x can be measured quite imprecisely, for example


#hot diggity damn kids what a fun project

plt.show()