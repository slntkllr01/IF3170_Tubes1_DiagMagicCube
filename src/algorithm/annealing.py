from utils.node import Node
import random
import math
import copy

class Annealing:
    def __init__(self, initial_temp, cooling_rate, schedule_type):
        self.Node = Node(cube_size=5)
        self.history = []
        self.historyvar = []
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.schedule_type = schedule_type
        self.stuck = 0
        self.history.append({
            "frame": 1,
            "cube": copy.deepcopy(self.Node.cube),
            "objective_value": self.Node.current_value
        })

    def linear_cooling(self, temp, iteration):
        return temp - self.cooling_rate * iteration

    def exponential_cooling(self, temp, iteration):
        return temp * (self.cooling_rate ** iteration)

    def logarithmic_cooling(self, temp, iteration):
        return temp / (1 + self.cooling_rate * math.log(1 + iteration))
    
    def quadratic_cooling(self, temp, iteration):
        return temp / (1 + self.cooling_rate * iteration * iteration)

    def simulatedAnnealing(self):
        print("Initial state of the cube:")
        self.Node.showCube()
        current_heuristic = self.Node.calculateHeuristic()
        initial = copy.deepcopy(self.Node)
        initial_heuristic = current_heuristic
        temp = self.initial_temp     
        i = 2
        while True:
            if temp <= 0:
                break
            neighbor = copy.deepcopy(self.Node.getRandomSuccessor())
            neighbor_heuristic = neighbor.calculateHeuristic()
            deltaE = neighbor_heuristic - current_heuristic

            if neighbor.current_value == 0:
                self.Node = neighbor
                self.history.append({"frame": i, "cube": copy.deepcopy(self.Node.cube),  "objective_value": self.Node.current_value})
                break

            if deltaE < 0:
                self.Node = neighbor
                current_heuristic = neighbor_heuristic
                print("Take good/better moves🫵🫵🫵")
                self.history.append({"frame": i, "cube": copy.deepcopy(self.Node.cube),  "objective_value": self.Node.current_value})
        
            else:
                self.stuck+=1
                rand = random.random()
                val = math.exp(-deltaE / temp)
                self.historyvar.append({"frame": i,"var_value": val})
                if  val > rand:
                    print("Take bad moves❌❌❌ with random: ", rand)
                    print("INI NILAI VAL🤯"+str(-1*deltaE / temp))
                    self.Node = neighbor
                    current_heuristic = neighbor_heuristic
                    self.history.append({"frame": i, "cube": copy.deepcopy(self.Node.cube),  "objective_value": self.Node.current_value})

                else:
                    print("FAILED TO USE ",val,"BAD MOVES🦋👺 with random ", rand, "and temp: ", temp)
            if self.schedule_type == "linear":
                temp = self.linear_cooling(temp, i)
            elif self.schedule_type == "exponential":
                temp = self.exponential_cooling(temp, i)
            elif self.schedule_type == "logarithmic":
                temp = self.logarithmic_cooling(temp, i)
            elif self.schedule_type == "quadratic":
                temp = self.quadratic_cooling(temp, i)
            i+=1
        
        print("Final state of the cube:")
        self.Node.showCube()
        print(f"Initial objective function value: {initial_heuristic}")
        print(f"Final objective function value: {current_heuristic}")
        print(f"Total iterations: {i}")
        print(f"Stuck in local optima: {self.stuck}")
        print("ini initial")
        initial.showCube()
        return self.Node