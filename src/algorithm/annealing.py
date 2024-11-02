from utils.node import Node
from utils.utility import Utility
import random
import math

class Annealing:
    def __init__(self, initial_temp, cooling_rate):
        self.Node = Node(cube_size=5)
        self.history = []
        self.initial_state = None
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate

    def linear_cooling(T_start, alpha, iteration):
        return T_start - alpha * iteration

    def simulatedAnnealing(self):
        current = self.Node
        current_heuristic = current.calculateHeuristic()
        temp = self.initial_temp     
        i = 0   
        while True:
            if temp <= 0:
                break
            neighbor = self.Node.getRandomSuccessor()
            neighbor_heuristic = neighbor.calculateHeuristic()
            # print("NILAI NEIGHBOR💖: ", neighbor_heuristic)
            # print("NILAI CURRENT💜: ", current_heuristic)
            deltaE = neighbor_heuristic - current_heuristic
            if deltaE > 0:
                current = neighbor
                current_heuristic = neighbor_heuristic
                print("Take good/better moves🫵🫵🫵")
            else:
                rand = random.random()
                val = math.exp(deltaE / temp)
                # print("Ini nilai val: ", val, " dengan deltaE: ", deltaE, "dan nilai temp: ", temp)
                # print("random values is ------------- ", rand, "compared with ---- ", math.exp(deltaE / temp))
                if  val > rand:
                    print("Take bad moves❌❌❌ with random: ", rand)
                    current = neighbor
                    current_heuristic = neighbor_heuristic
                else:
                    print("FAILED TO USE ",val,"BAD MOVES🦋👺 with random ", rand, "and temp: ", temp)
            self.history.append({"frame": 0, "cube": current.cube, "objective_value": current_heuristic})
            temp = temp - self.cooling_rate * i
            i+=1

        print("Final state of the cube:")
        current.showCube()
        print(f"Final objective function value: {current_heuristic}")
        print(f"Total iterations: {i}")
        return self.Node