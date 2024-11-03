from utils.node import Node
import random
import math

class Annealing:
    def __init__(self, initial_temp, cooling_rate, schedule_type):
        self.Node = Node(cube_size=5)
        self.history = []
        self.average = 0
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.schedule_type = schedule_type

    def linear_cooling(self, temp, iteration):
        return temp - self.cooling_rate * iteration

    def exponential_cooling(self, temp, iteration):
        return temp * (self.cooling_rate ** iteration)

    def logarithmic_cooling(self, temp, iteration):
        return self.initial_temp / (1 + self.cooling_rate * math.log(1 + iteration))
    
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
            deltaE = neighbor_heuristic - current_heuristic
            if deltaE > 0:
                current = neighbor
                current_heuristic = neighbor_heuristic
                print("Take good/better moves🫵🫵🫵")
                self.history.append({"frame": i, "cube": current.cube, "objective_value": current_heuristic})

            else:
                rand = random.random()
                val = math.exp(deltaE / temp)
                if  val > rand:
                    print("Take bad moves❌❌❌ with random: ", rand)
                    current = neighbor
                    current_heuristic = neighbor_heuristic
                    self.history.append({"frame": i, "cube": current.cube, "objective_value": current_heuristic})

                else:
                    print("FAILED TO USE ",val,"BAD MOVES🦋👺 with random ", rand, "and temp: ", temp)
            if self.schedule_type == "linear":
                temp = self.linear_cooling(temp, i)
            elif self.schedule_type == "exponential":
                temp = self.exponential_cooling(temp, i)
            elif self.schedule_type == "logarithmic":
                temp = self.logarithmic_cooling(temp, i)
            i+=1

        print("Final state of the cube:")
        current.showCube()
        print(f"Final objective function value: {current_heuristic}")
        print(f"Total iterations: {i}")
        return self.Node