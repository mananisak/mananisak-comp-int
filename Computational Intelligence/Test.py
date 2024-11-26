#SmartboGA is a GA that learns parameters for simple xpilot production system
#Manan Isak & Kate Le
#04/05/2022

#GENERAL IDEA
#Create 2 python files: SmartBo.py and agent.py
#SmartBo.py: run GA, start server, call agent.py to calculate fitnesses of all chroms
#agent.py: start xpilot agent, calculate fitness of a single chrom, terminate server  
#To run, first run SmartBo.py, inside SmartBo.py there is a command to run the terminal and agent.py
#Start out with 100 chrom in a text file (name it poptextfile.txt)
#Create 1 text file called temp.txt (to store the single chrom we're testing)
#Create 1 text file called fitnesses.txt (to store fitnesses of all chroms in a population)


#INSIDE SmartBo.py:
#Read all chroms in poptextfile.py
#For each chrom: 
#--Write current crom into temp.txt (this file is overwritten in every iteration as we test a new chrom)
#--Calculate fitness of this chrom by
#-----Starting a new server 
#-----Run agent.py


#INSIDE agent.py:
#-----Read the current chrom in temp.txt
#-----Decode the current chrom
#-----Get trackR, trackL, trackW, maxSpeed
#-----Start xpilot
#-----Count frames while xpilot runs 
#-----Terminate the server when xpilot dies (no need to quitAI())
#-----Get frames
#-----Fitness = frames * 10 + averageSpeed
#-----Append current fitness into fitnesses.txt


#BACK TO SmartBo.py:
#--Move on to a new chrom and repeat the steps
#Now we get fitnesses of all chroms in fitnesses.txt 
#Do the GA
#When you're done with GA, overwrite poptextfile.txt with new population
#Do it again until we reach the last generation


#HOW TO START & TERMINATE THE SERVER AND RUN ANOTHER PYTHON FILE FROM A PYTHON FILE
#Start the server: p1 = s.Popen("./xpilots -map maps/simple.xp -noQuit -switchBase 1 -maxClientsPerIP 32",shell = True)
#Terminate the server: s.Popen("pkill xpilots",shell=True) 
#Run a python file: p2 = s.Popen("python3 agent.py",shell = True)


#CODE
#agent.py code (half completed):
import random
#import libpyAI as ai
import subprocess as s
import time

#read chrom from temp.txt
#For example value of chrom should be like, chrom = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
#Then decode this chrom
#Call calcFitness(chrom)

def decode(chromosome):
	decodedChrom = []
	trackLeft = int(str("".join(str(x) for x in chromosome[:9])), 2)
	trackRight = int(str("".join(str(x) for x in chromosome[9:18])), 2)
	trackWall = int(str("".join(str(x) for x in chromosome[18:27])), 2)
	maxSpeed = int(str("".join(str(x) for x in chromosome[27:32])), 2)
	decodedChrom.append([trackLeft, trackRight, trackWall, maxSpeed])
	
	return decodedChrom

def calcFitness(chromosome):
    '''
    decChrom = decode(chromosome)
    time = 0
    trackR = decChrom[0][0]
    trackL = decChrom[0][1]
    trackW = decChrom[0][2]
    maxS = decChrom[0][3]
    countResult = runAI(trackR, trackL, trackW, maxS,0)

    #Calculate fitness here after server is terminated!
    #fitness = countResult*10 + averageSpeed
    #Append fitness to fitnesses.txt here

    return
    '''
    fitness = 0
    for bit in chromosome:
        if bit == 1:
            fitness = fitness + 1

    return fitness

frames = 0

def runAI(trackR, trackL, trackW, maxS, totalSpeed):
	def AI_loop():

		'''
		print(trackR)
		print(trackL)
		print(trackW)
		print(maxS)
		'''

		#Release keys
		ai.thrust(0)
		ai.turnLeft(0)
		ai.turnRight(0)

		#Set variables
		ai.setTurnSpeedDeg(20)
		heading = int(ai.selfHeadingDeg())
		tracking = int(ai.selfTrackingDeg())
		frontWall = ai.wallFeeler(1000,heading)
		leftWall = ai.wallFeeler(1000,heading+90) #Changed to 90 degrees
		rightWall = ai.wallFeeler(1000,heading-90)
		trackWall = ai.wallFeeler(1000,tracking)
		trackRight = ai.wallFeeler(1000,tracking-90)
		trackLeft = ai.wallFeeler(1000,tracking+90)
		selfSpeed = ai.selfSpeed()

		#Turning
		if leftWall < rightWall:
			ai.turnRight(1)
		elif leftWall > rightWall:
			ai.turnLeft(1)

		#Avoid Walls
		if trackRight < trackR or trackLeft < trackL:
			ai.thrust(1)
		elif trackWall < trackW:
			ai.thrust(1)
		if selfSpeed < maxS:
			ai.thrust(1)

		ai.fireShot()

		if (ai.selfAlive() == 0):
			s.Popen("pkill xpilots",shell=True)
			
		
		global frames #this is how Aartee increments variable 'count' inside AI_loop => it should work
		frames += 1

		print(frames)

		#print("Average speed:")
		#print(totalSpeed/frames)
		#print("frames:")
	
	ai.start(AI_loop,["-name","SmartBo","-join","localhost"])

	return frames


#SmartBo.py code (not completed):
#Create random chromosome
#Parameters are trackLeft(0-511), trackRight(0-511), trackWall(0-511), maxSpeed(0-31)
#trackLeft 9 bits, trackRight 9 bits, trackWall 9 bits, maxSpeed 5 bits. 32 bit chromosome
def genChrom(bits):
	chromosome = []

	for x in range(bits):
		chromosome.append(random.randint(0, 1))

	return chromosome

#Calculates the fittest chromosome
def calcFittest(population):
	fittest = population[0]
	for x in range(len(population)):
		if population[x][1] > fittest[1]:
			fittest = population[x]

	return fittest

#Returns total fitness of the population
def calcTotalFit(population):
	total = 0

	for entry in population:
		total = total + entry[1]

	return total

#Standard crossover
def crossover(parent1, parent2):
	child1 = []
	child2 = []
	crossPoint = random.randint(1, len(parent1)-1) #-1 Ensures cloning doesn't happen
	for x in range(len(parent1)):
		if x < crossPoint:
		    child1.append(parent1[x])
		    child2.append(parent2[x])
		else:
		    child1.append(parent2[x])
		    child2.append(parent1[x])

	return [child1, child2]

#Picks both parents and returns an array of their two locations with roulette wheel selection
def selection2(population, totalFitness):
	roulettePoint = random.randint(0, totalFitness)
	counter = 0

	for x in range(len(population)):
		counter = counter + population[x][1]
		if counter >= roulettePoint:
		    return x

def selection(population, totalFitness):
	parents = []
	parent1 = selection2(population, totalFitness)
	parent2 = selection2(population, totalFitness)
	#Guarantees the parents are different
	while parent2 == parent1:
		parent2 = selection2(population, totalFitness)

	parents.append(parent1)
	parents.append(parent2)

	return parents

#Mutation flips one bit fromt 0 to 1 or 1 to 0
def mutation(bit):
	if bit == 0:
		return 1
	else:
		return 0


#Parameters
bits = 32
n = 100
mutateRate = 0.001
crossRate = 1

#Create population of chromosomes paired with their fitness
population = []
for x in range(n):
	population.append([genChrom(bits), 0])
	population[x][1] = calcFitness(population[x][0])

#Start running
generation = 0

data = []
while calcFittest(population)[1] < bits:
	totalFitness = calcTotalFit(population)

	#Every hundred generations save the fittest chromosome, it's fitness, and the average fitness of the population
	data.append([calcFittest(population), totalFitness/n])

	#print("Generation: " + str(generation) + " Average Fitness: " + str(totalFitness/n) + " Fittest Fitness: " + str(calcFitness(calcFittest(population)[0])))
	tempPop = []
	for x in range(int(n/2)): #Each crossover produces 2 children
		#Selection
		parents = selection(population, totalFitness)

		#Crossover
		if random.random() < crossRate:
		    children = crossover(population[parents[0]][0], population[parents[1]][0])
		else:
		    children = [population[parents[0]][0], population[parents[1]][0]]


		#Mutation
		
		for child in children:
		    for i in range(bits):
		        if random.random() < mutateRate:
		            child[i] = mutation(child[i])

		#Repopulate
		tempPop.append([children[0], 0])
		tempPop.append([children[1], 0])

	#print(fitness(fittest(population))
	population = tempPop
	for x in range(n):
		population[x][1] = calcFitness(population[x][0])
	generation = generation + 1

data.append([calcFittest(population), totalFitness/n])
fittest = [str(int) for int in calcFittest(population)[0]]

print("Generation: " + str(generation) + " Average Fitness: " + str(totalFitness/n) + " Fittest Fitness: " + str(calcFittest(population)[1]))
print("".join(fittest))

#Saving the data to files
finalPopFile = open("FinalPop.txt", "w")
for chromosome in population:
	chromString = [str(int) for int in chromosome[0]]
	chromString = "".join(chromString)
	finalPopFile.write(chromString)
	finalPopFile.write("\n")
finalPopFile.close()

dataFile = open("Data.txt", "w")
for entry in data:
	entry[0] = [str(int) for int in entry[0]]
	dataFile.write("".join(entry[0]))
	dataFile.write(" ")
	dataFile.write(str(entry[1]))
	dataFile.write("\n")
dataFile.close()
