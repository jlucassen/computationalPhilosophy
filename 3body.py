from vpython import *
import matplotlib.pyplot as plt
import numpy as np

def nBody(bodyParams, t = 100, dt = 0.01): #simulates some mutually gravitating bodies for t time units, with discrete time step dt
    scene = canvas(height = 600, width = 600, align = 'left') #creates a new scene to host simulation
    for kwargs in bodyParams: #bodies are defined by a list of dictionaries - this prevents VPython from rendering stuff before start
        sphere(**kwargs)
    bodies = scene.objects
    for _ in arange(0, t, dt): #start simulation
        rate(100) #set frame rate
        forceDict = {}
        for attracted in bodies: #first loop is to calculate forces and modify velocities
            for attractor in bodies:
                if not attracted == attractor:
                    if not (attracted, attractor) in forceDict.keys(): #store forces, for if simulating lots of bodies
                        force = calculateForce(attracted, attractor)
                        attracted.vel += force*dt/attracted.m #dv = F*dt/m
                        forceDict[(attractor, attracted)] = -force
                    else:
                        attracted.vel += forceDict[(attracted, attractor)]*dt/attracted.m
        for b in bodies: #second loop is to update positions based on velocities
            b.pos += b.vel*dt

def calculateForce(body1, body2): #Just a formula plugin. Returns force of body2 on body1 as a vpython vector
    r = body2.pos-body1.pos
    rHat = r/mag(r)
    return body1.m*body2.m/(mag(r)**2)*rHat #force of gravity = Gmm/r^2, using G = 1 for convenience

def nBodyParallel(allBodyParams, t = 100, dt = 0.01): #Runs some number of simulations in parallel, each of which is basically an nBody
    canvasSize = int(1500/len(allBodyParams)) #calculate how big each canvas is going to have to be to fit on my screen
    spaces = []
    for spaceBodyParams in allBodyParams: #dig down first level, pulling a list of object parameter dictionaries out of allBodyParams
        spaces.append(canvas(height = canvasSize, width = canvasSize, align = 'left'))
        for bodyParams in spaceBodyParams: #dig down second level, pulling parameter dictionary out of spaceBodyParams
            sphere(**bodyParams)

    for _ in arange(0, t, dt): #start sim
        rate(100)
        for space in spaces: #in each time step, iterate through each scene
            bodies = space.objects #the rest of this is just nBody()
            forceDict = {}
            for attracted in bodies:
                for attractor in bodies:
                    if not attracted == attractor:
                        if not (attracted, attractor) in forceDict.keys():
                            force = calculateForce(attracted, attractor)
                            attracted.vel += force*dt/attracted.m
                            forceDict[(attractor, attracted)] = -force
                        else:
                            attracted.vel += forceDict[(attracted, attractor)]*dt/attracted.m
            for b in bodies:
                b.pos += b.vel*dt

def threeBodyPlus(bodyParams, t = 100, dt = 0.01, center = False, plane = False, norm = False): #simulates some mutually gravitating bodies for t time units, with discrete time step dt
    scene = canvas(height = 600, width = 600, align = 'left') #creates a new scene to host simulation
    for kwargs in bodyParams: #bodies are defined by a list of dictionaries - this prevents VPython from rendering stuff before start
        sphere(**kwargs)
    bodies = scene.objects

    if center: #if center is activated, create sphere at center of mass
        totalMass = bodies[0].m+bodies[1].m+bodies[2].m
        com = sphere(make_trail=True, radius=0.1, pos=vec((bodies[0].pos*bodies[0].m + bodies[1].pos*bodies[1].m + bodies[2].pos*bodies[2].m) / totalMass))
        if plane: #if plane is activated, create triangle with vertices at body
            tri = triangle(v0=vertex(pos=bodies[0].pos, color=bodies[0].color), v1=vertex(pos=bodies[1].pos, color=bodies[1].color), v2=vertex(pos=bodies[2].pos, color=bodies[2].color))
            if norm:
                bodies[0].make_trail = False
                bodies[1].make_trail = False
                bodies[2].make_trail = False
                com.make_trail = False

    for _ in arange(0, t, dt): #main simulation loop
        rate(100) #set frame rate
        forceDict = {}
        for attracted in bodies: #first loop is to calculate forces and modify velocities
            for attractor in bodies:
                if not attracted == attractor:
                    if not (attracted, attractor) in forceDict.keys(): #store forces, for if simulating lots of bodies
                        force = calculateForce(attracted, attractor)
                        attracted.vel += force*dt/attracted.m #dv = F*dt/m
                        forceDict[(attractor, attracted)] = -force
                    else:
                        attracted.vel += forceDict[(attracted, attractor)]*dt/attracted.m
        for b in bodies: #second loop is to update positions based on velocities
            b.pos += b.vel*dt
        
        if center: #update COM position if center turned on
            com.pos=vec((bodies[0].pos*bodies[0].m + bodies[1].pos*bodies[1].m + bodies[2].pos*bodies[2].m) / totalMass)
            if plane: #update tri corners if center and plane turned on
                tri.v0.pos = bodies[0].pos
                tri.v1.pos = bodies[1].pos
                tri.v2.pos = bodies[2].pos
                if norm: #move camera normal to tri if center and plane and norm turned on
                    normalAxis = cross(bodies[0].pos-com.pos, bodies[1].pos-com.pos).norm()*10
                    scene.camera.pos = com.pos + normalAxis
                    scene.camera.axis = -normalAxis

def plotDivergence(bodyParams, t=100, dt = 0.01, permutationFactors = [1, 1.01, 0.99, 1.02, 0.98]):
    out = {}
    if not permutationFactors[0] == 1:
        permutationFactors.insert(0, 1)
    for factor in permutationFactors: #iterate through all trials
        vectorRecord = {}
        scene = canvas(height = 600, width = 600, align = 'left') #creates a new scene to host simulation
        for kwargs in bodyParams: #bodies are defined by a list of dictionaries - this prevents VPython from rendering stuff before start
            sphere(**kwargs)
        bodies = scene.objects
        for body in bodies: #perturbs parameters based on factor
            body.pos *= factor
            body.vel *= factor
        for time in arange(0, t, dt): #start simulation
            rate(100) #set frame rate
            forceDict = {}
            for attracted in bodies: #first loop is to calculate forces and modify velocities
                for attractor in bodies:
                    if not attracted == attractor:
                        if not (attracted, attractor) in forceDict.keys(): #store forces, for if simulating lots of bodies
                            force = calculateForce(attracted, attractor)
                            attracted.vel += force*dt/attracted.m #dv = F*dt/m
                            forceDict[(attractor, attracted)] = -force
                        else:
                            attracted.vel += forceDict[(attracted, attractor)]*dt/attracted.m
            for b in bodies: #second loop is to update positions based on velocities
                b.pos += b.vel*dt
            vectorRecord[time] = (bodies[0].pos.x, #I hate this, this is terrible, ew ew ew 18-dimensional phase space
            bodies[0].pos.y,
            bodies[0].pos.z,
            bodies[0].vel.x*bodies[0].m,
            bodies[0].vel.y*bodies[0].m,
            bodies[0].vel.z*bodies[0].m,
            bodies[1].pos.x,
            bodies[1].pos.y,
            bodies[1].pos.z,
            bodies[1].vel.x*bodies[1].m,
            bodies[1].vel.y*bodies[1].m,
            bodies[1].vel.z*bodies[1].m,
            bodies[2].pos.x,
            bodies[2].pos.y,
            bodies[2].pos.z,
            bodies[2].vel.x*bodies[2].m,
            bodies[2].vel.y*bodies[2].m,
            bodies[2].vel.z*bodies[2].m)
        out[factor] = vectorRecord
    for factor in out.keys():
        dev = []
        for time in arange(0, t, dt):
            deviation = np.subtract(out[factor][time], out[1][time]) #find difference in phase space between current trial and "original"
            dev.append(sqrt(deviation[0]**2+deviation[1]**2+deviation[2]**2+deviation[3]**2+deviation[4]**2+deviation[5]**2+deviation[6]**2+deviation[7]**2+deviation[8]**2+deviation[9]**2+deviation[10]**2+deviation[11]**2+deviation[12]**2+deviation[13]**2+deviation[14]**2+deviation[15]**2+deviation[16]**2+deviation[17]**2))
        plt.plot(dev, label = str(factor))
    plt.legend()
    plt.yscale('log')
    plt.title('Divergence In Phase Space Over Time')
    plt.xlabel('Time Step')
    plt.ylabel('Log Phase Space Distance')
    plt.show()

b1d = {'color':color.red, 'make_trail':True, 'radius':0.5, 'm':1, 'pos':vec(-1,0,0), 'vel':vec(0,0.5,0)}
b2d = {'color':color.blue, 'make_trail':True, 'radius':0.5, 'm':1, 'pos':vec(1,0,0), 'vel':vec(0,-0.5,0)}
b3d = {'color':color.green, 'make_trail':True, 'radius':0.75, 'm':2, 'pos':vec(5,0,0), 'vel':vec(0,0,0.2)}
b1d2 = {'color':color.red, 'make_trail':True, 'radius':0.5, 'm':1, 'pos':vec(-1,0,0), 'vel':vec(0,0.51,0)}
b4d = {'color':color.yellow, 'make_trail':True, 'radius':0.3, 'm':0.5, 'pos':vec(0,0,1), 'vel':vec(0.1, 0,0)}

#nBodyParallel([[b1d, b2d, b3d], [b1d2,b2d,b3d], [b1d, b2d, b3d, b4d]])
#threeBodyPlus([b1d, b2d, b3d], center = True, plane = True, norm = True)
plotDivergence([b1d, b2d, b3d], t=200)
#nBody([{'color':color.red, 'make_trail':True, 'radius':0.5, 'm':1, 'pos':vec(-3,0,0), 'vel':vec(0,0.1,0)}, {'color':color.blue, 'make_trail':True, 'radius':0.5, 'm':1, 'pos':vec(3,0,0), 'vel':vec(0,0,0)}])