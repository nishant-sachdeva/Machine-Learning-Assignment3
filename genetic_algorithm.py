import client_moodle
import numpy as np
import random
import statistics
import geneticFunctions
import json

import pickle

populationSize = 30

f = open("overfit.txt", "r+")

num = f.read()

num = num.replace("[", " ")

num = num.replace("]", " ")

num = num.strip()

num = num.split(", ")

for i in range(0, len(num)):
    num[i]=float(num[i])

private_key="JVlzF9h4oeN3fyaOoSYgA1HiW82SlS1iptEqtB4lDQAeCK2k8C"


print(num)

population = []

try:
    with open('data.txt') as new_filename:
        population = json.load(new_filename)

except:
    print("the file did not load :/")
    for i in range(3):
        population.append(num)

    for i in range(0, populationSize-3):
        person = []
        for i in range(0, 11):
            gene = random.uniform(-10, 10)
            person.append(gene)
        population.append(person)



nextGenPopulation = []
for i in range(1, 40):
    print("Generation: "+str(i))
    # for i in range(0, populationSize):
    #     print(type(population[i]))
    fittestIndividualsForDirect, fittestIndividualsForCrossing, sortedFitnessValArray=geneticFunctions.naturalSelection(population, populationSize, private_key)
    nextGenPopulation=geneticFunctions.crossover(population, nextGenPopulation, populationSize, fittestIndividualsForDirect, fittestIndividualsForCrossing)
    nextGenPopulation=geneticFunctions.mutate(nextGenPopulation, populationSize)
    population=nextGenPopulation
    geneticFunctions.storeBestGeneration(population, sortedFitnessValArray[0])
    # print(str(statistics.median(thisGenTrain))+" "+str(statistics.median(thisGenValidation)))




# I have to find a way to make this population persistent
try:
    with open('data.txt' , "w") as f:
        json.dump(population , f)
        print(len(population))

except:
    print("the file did not load :/")
    print(population)

# this code should write my file into the j