import client_moodle
import random
import statistics
# import constants 

def naturalSelection(population, populationSize, private_key):
    prevGenFitnessTrain = []

    prevGenFitnessValidation = []


    for i in range(0, populationSize):
        try:
            temp = client_moodle.get_errors(private_key, population[i])
            print(str(i)+"th element's error for train and validation are " +str(temp[0])+" "+str(temp[1]))
        except:
            print("natural selection call did not work")
            temp = [1e40 , 1e40]
        
        prevGenFitnessTrain.append(temp[0])

        prevGenFitnessValidation.append(temp[1])
   
    # trainGuidelineUpper = 3625792
    # trainGuidelineLower = 79569
    # validationGuidelineUpper = 3625792

    # population = [x for _, x in sorted(zip(prevGenFitnessTrain, population))] 
    
    ####median method
    
    medTrainVal = statistics.median(prevGenFitnessTrain)

    medValidationVal = statistics.median(prevGenFitnessValidation)

    indexTrain=[]

    indexValidation=[]

    for i in range(0, populationSize):
        if prevGenFitnessTrain[i] > medTrainVal:
            indexTrain.append(i)
        if prevGenFitnessValidation[i] < medValidationVal:
            indexValidation.append(i)
    commonIndices = list(set(indexTrain).intersection(set(indexValidation)))

    return commonIndices, indexTrain, indexValidation, prevGenFitnessTrain, prevGenFitnessValidation 

def crossover(population, nextGenPopulation, populationSize, commonIndices, indexTrain, indexValidation):
    
    if len(commonIndices) > 0:
        for i in range(0, len(commonIndices)):
            nextGenPopulation.append(population[commonIndices[i]])

        symmetricDifferenceIndex = list(set(indexTrain).symmetric_difference(set(indexValidation)))

        for i in range(0, int((populationSize-len(commonIndices))/2)):
            tempArray = mate(population, symmetricDifferenceIndex)
            nextGenPopulation.append(tempArray[0])
            nextGenPopulation.append(tempArray[1])

        if len(nextGenPopulation)<populationSize:
            nextGenPopulation.append(mate(population, symmetricDifferenceIndex)[0])
    
    else:    
        unionIndex = list(set(indexTrain).union(set(indexValidation)))
        for i in range(0, int(populationSize/2)):
            tempArray = mate(population, unionIndex)
            nextGenPopulation.append(tempArray[0])
            nextGenPopulation.append(tempArray[1])
    return nextGenPopulation


def mate(population, symmetricDifferenceIndex):

    a = random.randint(0, len(symmetricDifferenceIndex)-1)
    b = random.randint(0, len(symmetricDifferenceIndex)-1)
    while b == a:
        b = random.randint(0, len(symmetricDifferenceIndex)-1)
    offSpring0=[]
    offSpring1=[]
    
    #####uniform crossover

    # for i in range(0, 11):
    #     coin = random.uniform(0, 1)
    #     if coin > 0.5:
    #         offSpring0.append(population[a][i])
    #         offSpring1.append(population[b][i])
    #     else:
    #         offSpring0.append(population[b][i])
    #         offSpring1.append(population[a][i])
    
    #####single-point crossover

    crossoverPoint = random.randint(0, 10)
    for i in range(0, 11):
        if i < crossoverPoint:
            offSpring0.append(population[a][i])
            offSpring1.append(population[b][i])
        else:
            offSpring0.append(population[b][i])
            offSpring1.append(population[a][i])

    #####double-point crossover

    # crossoverPoint0 = random.randint(0, 9)
    # crossoverPoint1 = random.randint(crossoverPoint0+1, 10)
    # for i in range(0, 11):
    #     if i < crossoverPoint0:
    #         offSpring0.append(population[a][i])
    #         offSpring1.append(population[b][i])
    #     elif i >= crossoverPoint0 and i < crossoverPoint1:
    #         offSpring0.append(population[b][i])
    #         offSpring1.append(population[a][i])
    #     else:
    #         offSpring0.append(population[a][i])
    #         offSpring1.append(population[b][i])

    offSprings = []
    offSprings.append(offSpring0)
    offSprings.append(offSpring1)
    return offSprings

def mutate(nextGenPopulation, populationSize):

    # int mutate_these_many = random.randrange(0, populationSize)
    
    # An alternate way of mutation : slightly less often ( it seems , but def more random)

    # for i in range(0, mutate_these_many):
    #     guy = random.randrange(0, populationSize)
    #     # so we mutate this Guy'th dude
    #     # in this guyth dude, we shall make some random number of genes

    #     int change_these_many_genes = random.randrange(0,11)

    #     for j in range(0,change_these_many_genes):
    #         gene = random.randrange(0,3)
    #         # now for this particular gene
    #         nextGenPopulation[guy][gene] = random.uniform(-10, 10)

    # return nextGenPopulation

    for i in range(0, populationSize):
        coin = random.uniform(0, 1)
        if coin > 0.95:
            for j in range(0, 11):
                coin1=random.uniform(0, 1)
                if coin1 > 0.95:
                    nextGenPopulation[i][j]=random.uniform(-10, 10)
    return nextGenPopulation
