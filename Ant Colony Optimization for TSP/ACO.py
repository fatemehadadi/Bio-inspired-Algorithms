import time
import random

# parameters
ANT_NUMBERS = 29
STEP_NUMBER = 200
INITIAL_PHEROMONE = 10
ALPHA = 1.0
P = 0.1  # evaporate rate
W = 0.9  # pheromone increase rate

# the main class with two sub classes: Ant and Colony
class ACO_TSP:
    class Colony:
        def __init__(self, nodes: int, dis):
            self.nodes = nodes
            self.pheromoneMatrix = [[0 for k in range(nodes)] for i in range(nodes)]
            self.distance = dis
            return

        def showBestTour(self):
            Tour = [0]
            dis = 0
            while len(Tour) < self.nodes:
                i = Tour[-1]
                unseen = []
                for j in range(self.nodes):
                    if j not in Tour:
                        unseen.append(j)
                maxPheromone = 0
                nextNode = unseen[0]
                for j in unseen:
                    if self.pheromoneMatrix[j][i] > maxPheromone:
                        nextNode = j
                        maxPheromone = self.pheromoneMatrix[j][i]
                Tour.append(nextNode)
                if i < nextNode:
                    dis += int(self.distance[i][(nextNode - i) - 1])
                else:
                    dis += int(self.distance[nextNode][i - nextNode - 1])
            if Tour[-1] < Tour[0]:
                dis += int(self.distance[Tour[-1]][(Tour[0] - Tour[-1]) - 1])
            else:
                dis += int(self.distance[Tour[0]][Tour[-1] - Tour[0] - 1])
            return Tour, dis

    class Ant:
        def __init__(self):
            self.age = 0
            self.startNode = 0
            self.currentNode = 0
            self.lastTour = []  # a permutation
            self.lastTourFit = 0.0
            return

        def makeTour(self, colony, size):
            self.lastTour = []  # a permutation
            self.lastTourFit = 0.0
            self.startNode = random.randint(0, size - 1)
            tour = [self.startNode]
            cuurent = self.startNode
            for i in range(size-1):
                # select the next node in the tour
                unseen = []
                # node = tour[i]
                for j in range(size):
                    if j not in tour:
                        unseen.append(j)

                sumPheromones = 0
                for j in unseen:
                    # calculate the sum of pheromones
                    sumPheromones += pow(colony.pheromoneMatrix[cuurent][j], ALPHA)
                if sumPheromones == 0:
                    print("error", unseen)
                dictUnseen = {}
                probabilityList = []
                for j in unseen:
                    dictUnseen[pow(colony.pheromoneMatrix[i][j], ALPHA) / sumPheromones] = j
                    probabilityList.append(pow(colony.pheromoneMatrix[i][j], ALPHA) / sumPheromones)
                probabilityList=sorted(probabilityList)
                probabilityList = probabilityList[::-1]
                # print(probabilityList)
                random_value = random.uniform(0.0, 100)
                choice = 0
                for j in probabilityList:
                    if j > random_value:
                        choice = dictUnseen[j]
                if choice == 0:
                    choice = dictUnseen[probabilityList[random.randint(0,len(probabilityList)-1)]]
                tour.append(choice)
                cuurent = choice
            self.lastTour = tour
            self.lastTourFit = self.evaluateTour(colony)

            return

        def evaluateTour(self, colony):
            cost = 0
            for i in range(len(self.lastTour)):

                if i == len(self.lastTour) - 1:
                    nextNode = self.lastTour[0]
                else:
                    nextNode = self.lastTour[i + 1]

                if self.lastTour[i] < nextNode:
                    cost += int(colony.distance[self.lastTour[i]][(nextNode - self.lastTour[i]) - 1])
                else:
                    cost += int(colony.distance[nextNode][self.lastTour[i] - nextNode - 1])
            return (1 / cost) * 100000

    def __init__(self, datasetFile):
        with open(datasetFile) as f:
            data = [line.rstrip().split() for line in f]
        distance = []
        for i in data:
            if i[0] == "DISPLAY_DATA_SECTION":
                break
            if i[0].isnumeric():
                distance.append(i)
        distance.append([])
        self.colonySize = len(distance)
        self.colony = self.Colony(len(distance), distance)
        self.ants = [self.Ant() for _ in range(ANT_NUMBERS)]
        self.bestTour = []
        self.bestFitness = 0
        return

    def evaporatePheromone(self):
        for i in range(self.colonySize):
            for j in range(self.colonySize):
                self.colony.pheromoneMatrix[i][j] = (1 - P) * self.colony.pheromoneMatrix[i][j]
                self.colony.pheromoneMatrix[j][i] = (1 - P) * self.colony.pheromoneMatrix[j][i]
        return

    def updatePheromone(self, ant):
        tour = ant.lastTour
        for i in range(self.colonySize):
            if i == self.colonySize - 1:
                self.colony.pheromoneMatrix[tour[i]][tour[0]] += ant.evaluateTour(self.colony)*W
                self.colony.pheromoneMatrix[tour[0]][tour[i]] += ant.evaluateTour(self.colony)*W
            else:
                self.colony.pheromoneMatrix[tour[i]][tour[i + 1]] += ant.evaluateTour(self.colony)*W
                self.colony.pheromoneMatrix[tour[i + 1]][tour[i]] += ant.evaluateTour(self.colony)*W
        return

    def update_minPath(self, tour, fit):
        for i in range(self.colonySize):
            if i == self.colonySize - 1:
                self.colony.pheromoneMatrix[tour[i]][tour[0]] += fit
                self.colony.pheromoneMatrix[tour[0]][tour[i]] += fit
            else:
                self.colony.pheromoneMatrix[tour[i]][tour[i + 1]] += fit
                self.colony.pheromoneMatrix[tour[i + 1]][tour[i]] += fit

    def initialize_colony(self):
        for i in range(self.colonySize):
            for j in range(self.colonySize):
                if i != j :
                    self.colony.pheromoneMatrix[i][j] = INITIAL_PHEROMONE
                    self.colony.pheromoneMatrix[j][i] = INITIAL_PHEROMONE
        return

    def run(self):
        self.initialize_colony()
        for k in range(STEP_NUMBER):
            print("round",k, end="   ")
            local_best_tour = []
            local_best_fit = 0
            for ant in self.ants:
                ant.makeTour(self.colony, self.colonySize)
                self.updatePheromone(ant)
                if ant.lastTourFit > local_best_fit:
                    local_best_fit = ant.lastTourFit
                    local_best_tour = ant.lastTour

            self.update_minPath(local_best_tour, local_best_fit)

            tour, dis = self.colony.showBestTour()
            print( "best fitness: ",round((1 / dis) * 100000,3))

            if self.bestFitness < (1 / dis) * 100000:
                self.bestFitness = (1 / dis) * 100000
                self.bestTour = tour

        print("---------------------------------------------------------------------------")
        print("best answer: ", end = "")
        print(self.bestTour,"fitness:", round(self.bestFitness,3))
        return


if __name__ == "__main__":
    start_time = time.clock()
    tsp = ACO_TSP("bayg29.tsp")
    tsp.run()
    end_time = time.clock()
    print("duration:", round((end_time - start_time), 3), "s")
