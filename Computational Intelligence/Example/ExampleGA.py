#Example GA to make a chromosome of all 1s
#Manan Isak
#Oct 11 2023

import random

#Fitness is the sum of 1s
def calcFitness(chromosome):
	fitness = sum([sum(gene) for gene in chromosome])
	return fitness

def calcFitnesses(population):
	fitnesses = map(calcFitness, population)
	return list(fitnesses)

#Roulette wheel selection
def selection(population, fitnesses):
	parent1, parent2 = selection2(fitnesses), selection2(fitnesses)
	
	#Ensure the parents are different
	while parent2 == parent1:
		parent2 = selection2(fitnesses)

	return [population[parent1],population[parent2]]

def selection2(fitnesses):
	roulettePoint = random.uniform(0, sum(fitnesses))
	counter = 0
	
	for x in range(len(fitnesses)):
		counter = counter + fitnesses[x]
		if counter >= roulettePoint:
			return x

#Uniform crossover, returns one child
def crossover(parents):
	child = []
	for gene in range(len(parents[0])):
		child.append([])
		for bit in range(len(parents[0][gene])):
			whichParent = random.randint(0,1)
			child[gene].append(parents[whichParent][gene][bit])
	return child
	
def mutation(chromosome, mutateRate):
	tempChrom = []
	
	for gene in range(len(chromosome)):
		#Intra-gene
		if random.random() < mutateRate:
			tempChrom.append(makeChrom([len(chromosome[gene])])[0])
		#Inter-gene
		else:
			tempChrom.append(chromosome[gene])
			for bit in range(len(chromosome[gene])):
				if random.random() < mutateRate:
					tempChrom[gene][bit] = (tempChrom[gene][bit]+1)%2
	return tempChrom

def makeChrom(genes):
	chromosome = []
	for gene in range(len(genes)):
		chromosome.append([])
		for bit in range(genes[gene]):
			chromosome[gene].append(random.randint(0,1))
	return chromosome

def makePop(n, genes):
	return [makeChrom(genes) for _ in range(n)]
	
def getFittest(population, fitnesses):
	return population[fitnesses.index(max(fitnesses))]

GENES = [64]
GENERATIONCOUNT = 500
POPULATIONSIZE = 100
CROSSOVERRATE = 1
MUTATERATE = 0.001
genDetails = ""

#Read initial population from a file?
try:
	fileRead = eval(input("Read population from file? "))
except:
	fileRead = False

if fileRead:
	file = open("Population.txt", "r")
	population = eval(file.read())
	file.close()
else:
	population = makePop(POPULATIONSIZE, GENES)

#Start training
for generation in range(1, GENERATIONCOUNT+1):
	#Calculate fitnesses
	fitnesses = calcFitnesses(population)
	
	#Save the generation details every x generations
	if generation%1 == 0:
		genDetails += f"{generation} {max(fitnesses)} {sum(fitnesses)/POPULATIONSIZE} {getFittest(population, fitnesses)}\n"
		print(f"{generation} {max(fitnesses)} {sum(fitnesses)/POPULATIONSIZE} {getFittest(population, fitnesses)}")

	tempPop = []
	
	#Selection, crossover, mutation, repopulation
	for i in range(POPULATIONSIZE):
		parents = selection(population,fitnesses)

		#If crossover doesn't happen, choose a random parent
		if random.random() <= CROSSOVERRATE:
			child = crossover(parents)
		else:
			child = parents[random.randint(0,1)]

		child = mutation(child, MUTATERATE)
		tempPop.append(child)

	population = tempPop

#Write population to a file
popFile = open("Population.txt", "w")
popFile.write(str(population))
popFile.close()

#Write to a file
fitnessFile = open("GenDetails.txt", "w")
fitnessFile.write(genDetails)
fitnessFile.close()