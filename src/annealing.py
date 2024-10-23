from utils import *
import math
import time
class Annealing:
    def simulatedAnnealing(cube_size, initial_temp, cooling_rate):
        current = Node(cube_size)
        current_heuristic = current.calculateHeuristic()
        temp = initial_temp
        
        # will stop if temperature is 0 
        start = time.time()
        while True:
            if (temp<=0):
                break
            neighbor = Node(cube_size)
            Utility.swapElement(neighbor.cube)
            neighbor_heuristic = neighbor.calculateHeuristic()
            deltaE = neighbor_heuristic-current_heuristic
            if (deltaE>0):
                current = neighbor
            else:
                if (math.exp(deltaE/temp)>random.random()):
                    current = neighbor
            temp *= cooling_rate
                
        end = time.time()
        time_elapsed = end-start
        print("Time elapsed: " + str(time_elapsed))
        return (current,time_elapsed)

