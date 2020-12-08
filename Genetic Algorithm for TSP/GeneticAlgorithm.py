import numpy as np
import math
from random import shuffle, randrange
from copy import deepcopy

# set parameters
MUTATION_RATE = 30  # percent of the children that face mutation
PRODUCTION_RATE = 50 # percentage of reproduction new children
SELECTION_PRESSURE = 40 # (0,100] is the percentage of pressure of selection, the greater number the less pressure
populationCount = 300 # the size of population
GenerationCount = 200 # number of evoluation cycle


def evaluate_fitness(path, distance):
    cost = 0
    for i in range(len(path)):
        if i == len(path)-1:
            cost+= int(distance[path[i]][path[0]])
            continue
        cost+= int(distance [path[i]][path[i+1]])
    return (1/cost)*100000


class Chromosome():
    def __init__(self):
        self.path = []
        self.fitness = 0

    def __init__(self, p, distance):
        self.path = deepcopy(p)
        self.fitness = evaluate_fitness(p, distance)


def is_there_path(p, pop):
    for gene in pop:
        if gene.path == p:
            return True
    return False


def initializer(cities, distance):
    chrom = Chromosome(cities, distance)
    pop = [chrom]
    for i in range(populationCount - 1):
        newPath = cities
        while is_there_path(newPath, pop):
            shuffle(newPath)
        pop.append(Chromosome(newPath, distance))
    return pop

def FindBestPath(pop):
    maxfit = pop[0].fitness
    path = pop[0].path
    for chrome in pop:
        if chrome.fitness > maxfit:
            maxfit = chrome.fitness
            path = chrome.path
    return path

def crossover_mutation(parents, distance):
    child = [-1 for i in parents[0].path]
    crosspoint = randrange(0, len(child)-4)
    for i in range(0,4):
        child[crosspoint+i]=parents[0].path[crosspoint+i]
    itterator = crosspoint+4
    readpoint = crosspoint+4
    while child[itterator] == -1:
        if parents[1].path[readpoint] in child:
            readpoint+=1
            if readpoint == len(child):
                readpoint=0
        else:
            child[itterator]= parents[1].path[readpoint]
            readpoint += 1
            if readpoint == len(child):
                readpoint = 0
            itterator +=1
            if itterator == len(child):
                itterator=0

    # mutation
    if randrange(0,100)< MUTATION_RATE:
        point1= randrange(0,len(child))
        point2= randrange(0, len(child))
        while point1!=point2:
            point2 = randrange(0, len(child))
        # swap two points
        child[point2], child[point1] = child[point1], child[point2]
    child = Chromosome(child, distance)
    return child

def sort_fitness(pop):
    for i in range(0, len(pop)-1):
        maxfit = pop[i].fitness
        index = i
        for j in range(i,len(pop)-1):
            if pop[j].fitness > maxfit:
                maxfit = pop[i].fitness
                index = j
        pop[i], pop[index] = pop[index], pop[i]
    return pop

def show_path( p ):
    for i in p :
        print(i+1, end ="->")
    print(p[0]+1)
    return
def run_GA(filename):
    with open(filename) as f:
        distance = [line.rstrip().split() for line in f]
    cities_n = len(distance[0])  # number of cities
    cities = list(range(cities_n))
    population = initializer(cities, distance)
    counter = 0
    bestChrom = Chromosome(FindBestPath(population), distance)
    print("first generation", counter, "| best fitness:", round(bestChrom.fitness), "|", end=" ")
    show_path(bestChrom.path)
    while counter < GenerationCount:
        # sort the population by the fitness of chromosome
        population = sort_fitness(population)

        # reproduction of chromosomes
        for k in range(0,int(populationCount*PRODUCTION_RATE/100)):
            # selection is truncation
            father = randrange(0,populationCount*SELECTION_PRESSURE/100)
            mother = randrange(0,populationCount*SELECTION_PRESSURE/100)
            parents = [population[father], population[mother]]
            child = crossover_mutation(parents, distance)
            population.append(child)

        # sort the new generation
        population = sort_fitness(population)

        # eliminate the worst fitness chromosome to maintain the population size
        population = population[0:populationCount]
        # debug massage
        bestChrom = Chromosome(FindBestPath(population), distance)
        print("generation#:",counter+1, "| best fitness:", round(bestChrom.fitness,2), "|", end=" ")
        show_path(bestChrom.path)
        counter+=1
    print("-----------------------------------------------------------------------------")
    print("Best solution:")
    show_path(bestChrom.path)
    print("best fitness:",round(bestChrom.fitness,2))
    return


if __name__ == "__main__":

    run_GA("Data1.txt")
