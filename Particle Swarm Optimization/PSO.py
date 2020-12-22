import numpy as np
import math
import time


def func(n, x, y):
    calc = 0
    if n == 1:
        # function 1
        calc = abs(1 - math.sqrt(math.pow(x, 2) + math.pow(y, 2)) / math.pi)
        calc = math.exp(calc)
        calc = abs(math.cos(x) * math.sin(y) * calc) * -1
    elif n == 2:
        # function 2
        calc = math.pow(math.cos(math.sin(abs(math.pow(x, 2) - math.pow(y, 2)))), 2) - 0.5
        calc = calc / math.pow(1 + 0.001 * (math.pow(x, 2) + math.pow(y, 2)), 2)
        calc = calc + 0.5

    return calc


class Particle:

    def __init__(self, n, max, min):
        self.n = n
        self.position = np.random.rand(2) * (max - min) + min
        self.velocity = np.random.rand(2) * (max - min) + min
        self.pBest = self.position
        self.min = min
        self.max = max
        self.fitBest = func(n, self.position[0], self.position[1])

    def update_position(self):
        self.position += self.velocity
        if self.position[0] < self.min:
            self.position[0] = self.min
        elif self.position[0] > self.max:
            self.position[0] = self.max
        if self.position[1] < self.min:
            self.position[1] = self.min
        elif self.position[1] > self.max:
            self.position[1] = self.max
        new_fit = func(self.n, self.position[0], self.position[1])
        if new_fit < self.fitBest:
            self.pBest = self.position
            self.fitBest = new_fit
        return self.position, self.fitBest

    def update_velocity(self, c, c1, c2, gBest):
        r11 = np.random.random()
        r21 = np.random.random()
        self.velocity[0] = (c * self.velocity[0] +
                            c1 * r11 * (self.pBest[0] - self.position[0]) +
                            c2 * r21 * (gBest[0] - self.position[0]))
        r12 = np.random.random()
        r22 = np.random.random()
        self.velocity[1] = (c * self.velocity[1] +
                            c1 * r12 * (self.pBest[1] - self.position[1]) +
                            c2 * r22 * (gBest[1] - self.position[1]))


def PSO(steps, swarm_size, c, c1, c2, type, max, min):
    init = Particle(type, max, min)
    swarm = [init]
    global_best_position = init.pBest
    global_best_fitness = init.fitBest
    for _ in range(swarm_size - 1):
        p = Particle(type, max, min)
        if p.fitBest < global_best_fitness:
            global_best_position = p.pBest
            global_best_fitness = p.fitBest
        swarm.append(p)
    for _ in range(steps):
        for particle in swarm:
            particle.update_velocity(c, c1, c2, global_best_position)
            new_position, new_fit = particle.update_position()
            if new_fit < global_best_fitness:
                global_best_position = new_position
                global_best_fitness = new_fit
    return np.round(global_best_position, 5), round(global_best_fitness, 3)


if __name__ == "__main__":
    start_time = time.process_time()
    # type 1 is for the first function optimization and type 2 is for the second function optimization
    result = PSO(steps=100, swarm_size=1000, c=0.5, c1=0.5, c2=0.2, type=2, max=100, min=-100)
    print("Minimum point:", result[0], "\nMinimum value:", result[1])
    end_time = time.process_time()
    print("duration:", round((end_time - start_time), 3), "s")
