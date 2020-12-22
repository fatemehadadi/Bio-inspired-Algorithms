import numpy as np
import math
from random import shuffle, randrange, randint
from copy import deepcopy
import time

# set parameters
num_samples = 10000


def evaluate_energy(path, distance):
    cost = 0
    for i in range(len(path)):
        if i == len(path) - 1:
            if path[i] < path[0]:
                cost += int(distance[path[i]][(path[0] - path[i]) - 1])
            else:
                cost += int(distance[path[0]][(path[i] - path[0]) - 1])
            continue
        if path[i] < path[i + 1]:
            cost += int(distance[path[i]][(path[i + 1] - path[i]) - 1])
        else:
            cost += int(distance[path[i + 1]][path[i] - path[i + 1] - 1])
    return cost


class State:
    def __init__(self):
        self.path = []
        self.energy = 0

    def __init__(self, p, distance):
        self.path = deepcopy(p)
        self.energy = evaluate_energy(p, distance)


def show_path(p):
    for i in p:
        print(i + 1, end="->")
    print(p[0] + 1)
    return

def temperature(curr, total):
    return 1 - (curr / total)


def random_neighbor(state, distance):
    # 2-opt
    p = deepcopy(state.path)
    l = randint(2, len(p) - 1)
    i = randint(0, len(p) - l)
    p[i: (i + l)] = reversed(p[i: (i + l)])
    rand_state = State(p, distance)
    return rand_state


def run_SA(filename):
    with open(filename) as f:
        data = [line.rstrip().split() for line in f]
    distance = []
    for i in data:
        if i[0] == "DISPLAY_DATA_SECTION":
            break
        if i[0].isnumeric():
            distance.append(i)
    distance.append([])
    cities_n = len(distance)  # number of cities
    start_state = State(list(range(cities_n)), distance)
    curr_state = start_state
    best_state = curr_state
    for i in range(num_samples):
        T = temperature(i, num_samples)
        new_state = random_neighbor(curr_state, distance)
        if new_state.energy <= curr_state.energy:
            curr_state = new_state
            if best_state.energy > new_state.energy:
                best_state = new_state
        else:
            delta = new_state.energy - curr_state.energy
            if np.random.random() < math.exp(-delta / T):
                curr_state = new_state
    return best_state


if __name__ == "__main__":
    start_time = time.process_time()
    result = run_SA("bayg29.tsp")
    show_path(result.path)
    print("cost:",result.energy,"|   fitness:" ,round((1 / result.energy) * 100000, 3))
    end_time = time.process_time()
    print("duration:", round((end_time - start_time), 3), "s")
