from utils.node import Node
from utils.utility import Utility
import random
import math

class Annealing:
    def __init__(self, initial_temp, cooling_rate):
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate

    def simulatedAnnealing(self):
        current = Node(cube_size=5)
        current_heuristic = current.calculateHeuristic()
        temp = self.initial_temp        
        while True:
            if temp <= 0:
                break
            neighbor = Node(cube_size=5)
            Utility.swapElement(neighbor.cube)
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
                print("random values is ------------- ", rand, "compared with ---- ", math.exp(deltaE / temp))
                if  val > rand:
                    print("Take bad moves❌❌❌ with random: ", rand)
                    current = neighbor
                    current_heuristic = neighbor_heuristic
                else:
                    print("FAILED TO USE ",val,"BAD MOVES🦋👺 with random ", rand, "and temp: ", temp)
            temp *=self.cooling_rate
                
        return current