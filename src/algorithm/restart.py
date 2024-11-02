from utils.node import Node
import matplotlib.pyplot as plt

class RandomRestart:
    def __init__(self):
        self.history = []
        self.initial_state = None 

    def solveCube(self, maxRestart):
        print("Starting search process (Random Restart Hill-Climbing)")
        print(f"Maximum restarts allowed: {maxRestart}")
        
        currvalue = float('inf')
        currcube = None
        self.initial_state = None 

        for i in range(maxRestart):
            RandomNode = Node(cube_size=5)
            if i == 0:
                self.initial_state = RandomNode  

            iterations = 0

            while iterations<1000:
                neighbour = RandomNode.getHighestSuccessor()
                iterations += 1

                if neighbour.current_value < RandomNode.current_value:
                    neighbour2 = neighbour.getHighestSuccessor()

                    if neighbour2.current_value < RandomNode.current_value:
                        RandomNode = neighbour2  
                    else:
                        RandomNode = neighbour 
                else:
                    break  

            if RandomNode.current_value < currvalue:
                currvalue = RandomNode.current_value
                currcube = RandomNode
                print(f"New best value found: {currvalue} (Restart {i + 1}, Iterations: {iterations})")
                self.history.append({"frame": i + 1, "cube": currcube.cube, "iterations": iterations, "objective_value": currvalue})

            if i + 1 == maxRestart:
                print("Maximum restarts reached, stopping search.")
                break

        print(f"Initial state of the cube: ")
        self.initial_state.showCube()
        print(f"Final state of the cube: ")
        currcube.showCube()
        print(f"Final objective function value achieved: {currvalue}")
        print(f"Total restarts: {i + 1}")

        return currcube
