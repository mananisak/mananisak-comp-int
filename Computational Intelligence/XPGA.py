#XPGA program to learn the parameters for an expert system for the Xpilot AI
#Manan Isak
#03/08/2022

#Framrate paper https://oak.conncoll.edu/parker/papers/SMC2011_Xpilot-AI.pdf

import random

#Generate a random gene. Each gene represents one parameter value in binary
def genGene(geneNum):
    genes = []

    for x in range(geneNum):
        chromosome.append(random.randint(0, 1))

    return genes

#Create a random chromosome of genes
def genChrom(bits):
    chromosome = []

    for x in range(bits):
        chromosome.append(random.randint(0, 1))

    return chromosome

#Calculates one fitness based on how long the xpilot lasts (number of frames squared)
def calcFitness(chromosome):
    fitness = 0
    for bit in chromosome:
        if bit == 1:
            fitness = fitness + 1

    return fitness

#Calculates all of the fitnesses into an array
def calcFitnesses(population):
    fitnesses = []
    for chromosome in population:
        fitnesses.append(calcFitness(chromosome))

    return fitnesses

#Calculates the fittest chromosome
def calcFittest(population, fitnesses):
    fittest = population[0]
    fittnessest = calcFitness(fittest)
    for x in range(len(population)):
        if fitnesses[x] > fittnessest:
            fittest = population[x]
            fittnessest = calcFitness(fittest)

    return fittest

#Returns total fitness of the population
def calcTotalFit(fitnesses):
    total = 0
    
    for fitness in fitnesses:
        total = total + fitness

    return total

#Standard crossover
def crossover(parent1, parent2):
    child1 = []
    child2 = []
    crossPoint = random.randint(1, len(parent1)-1) #Ensures cloning doesn't happen
    for x in range(len(parent1)):
        if x < crossPoint:
            child1.append(parent1[x])
            child2.append(parent2[x])
        else:
            child1.append(parent2[x])
            child2.append(parent1[x])
    
    return [child1, child2]

#Picks both parents and returns an array of their two locations with roulette wheel selection
def selection2(fitnesses, totalFitness):
    roulettePoint = random.randint(0, totalFitness)
    counter = 0

    for x in range(len(fitnesses)):
        counter = counter + fitnesses[x]
        if counter >= roulettePoint:
            return x

def selection(fitnesses, totalFitness):
    parents = []
    parent1 = selection2(fitnesses, totalFitness)
    parent2 = selection2(fitnesses, totalFitness)
    #Guarantees the parents are different
    while parent2 == parent1:
        parent2 = selection2(fitnesses, totalFitness)

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
bits = 64
n = 100
mutateRate = 0.001
crossRate = 1

#Create population of chromosomes
population = []
for x in range(n):
    population.append(genChrom(bits))

#Start running
generation = 0
fitnesses = calcFitnesses(population)
data = []
while calcFitness(calcFittest(population, fitnesses)) < bits:
    totalFitness = calcTotalFit(fitnesses)
    
    #Every hundred generations save the fittest chromosome, it's fitness, and the average fitness of the population
    if generation%100 == 0:
        data.append([calcFittest(population, fitnesses), calcFitness(calcFittest(population, fitnesses)), totalFitness/n])
    
    #print("Generation: " + str(generation) + " Average Fitness: " + str(totalFitness/n) + " Fittest Fitness: " + str(calcFitness(calcFittest(population, fitnesses))))
    tempPop = []
    for x in range(int(n/2)): #Each crossover produces 2 children
        #Selection
        parents = selection(fitnesses, totalFitness)

        #Crossover
        if random.random() <= crossRate:
            children = crossover(population[parents[0]], population[parents[1]])
        else:
            children = [population[parents[0]], population[parents[1]]]


        #Mutation
        
        for child in children:
            for i in range(bits):
                if random.random() < mutateRate:
                    child[i] = mutation(child[i])

        #Repopulate
        tempPop.append(children[0])
        tempPop.append(children[1])

    #print(fitness(fittest(population))
    population = tempPop
    fitnesses = calcFitnesses(population)
    generation = generation + 1

data.append([calcFittest(population, fitnesses), calcFitness(calcFittest(population, fitnesses)), totalFitness/n])
fittest = [str(int) for int in calcFittest(population, fitnesses)]

print("Generation: " + str(generation) + " Average Fitness: " + str(totalFitness/n) + " Fittest Fitness: " + str(calcFitness(calcFittest(population, fitnesses))))
print("".join(fittest))

#Saving the data to files
finalPopFile = open("FinalPop.txt", "w")
for chromosome in population:
    chromString = [str(int) for int in chromosome]
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
    dataFile.write(" ")
    dataFile.write(str(entry[2]))
    dataFile.write("\n")
dataFile.close()
