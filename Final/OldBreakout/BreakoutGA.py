#BreakoutGA program to learn the weights for an ANN Breakout controller
#Manan Isak & Kate Le
#04/25/2022

import sys, pygame, random, math, breakout

#Every 4 bits is a weight
def decodeChrom(chromosome):
    weights = [[0] * 6 for i in range(8)] #5 input + 1 threshold weight for 8 nodes
    excessX = -4
    counter = 0
    for x in range(8): #Per row/node
        for y in range(6): #Per column/weight
            weights[x][y] = int(str("".join(str(x) for x in chromosome[counter:counter+4])), 2) + excessX
            counter += 4

    return weights
    
#Create a random chromosome
def genChrom(bits):
    chromosome = []

    for x in range(bits):
        chromosome.append(random.randint(0, 1))

    return chromosome

#Calculates one fitness based on the Breakout score. We only want to run this once for each chromosome to save runtime. No repeats.
def calcFitness(chromosome):
    weights = decodeChrom(chromosome)
    #Run breakout using these weights
    
    #
    # run breakout game
    # while lives != 0
    # for each frame get 5 inputs 

    # call ANN, pass 5 inputs
    # Get 3 outpus
    # pass them into breakout game

    breakout.Breakout().main(weights)
    f = open("fit.txt", "r")
    fitness = int(f.read())
    f.close()
    
    return fitness
    
#Calculates all of the fitnesses into an array
def calcFitnesses(population):
    fitnesses = []
    for chromosome in population:
        fitnesses.append(calcFitness(chromosome))

    print("test")

    return fitnesses

#Calculates the fittest chromosome
def calcFittest(population, fitnesses):
    fittestChrom = population[0]
    fittestFitness = fitnesses[0]
    for x in range(len(population)):
        if fitnesses[x] > fittestFitness:
            fittestChrom = population[x]
            fittestFitness = fitnesses[x]

    return fittestChrom #, fittestFitness

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
bits = 192
n = 10
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
while generation < 4:
    totalFitness = calcTotalFit(fitnesses)
    
    #Every hundred generations save the fittest chromosome, it's fitness, and the average fitness of the population
    if generation%100 == 0:
        data.append([calcFittest(population, fitnesses), max(fitnesses), totalFitness/n])
    
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
    #Training
    population = tempPop
    fitnesses = calcFitnesses(population)
    generation = generation + 1

data.append([calcFittest(population, fitnesses), max(fitnesses), totalFitness/n])

fittest = [str(int) for int in calcFittest(population, fitnesses)]

print("Generation: " + str(generation) + " Average Fitness: " + str(totalFitness/n) + " Fittest Fitness: " + str(max(fitnesses)))
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
