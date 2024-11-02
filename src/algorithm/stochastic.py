from utils.node import Node

class Stochastic:
    def __init__(self):
        self.Node = Node(cube_size=5)
        self.history = []  
        self.initial_state = self.Node  

    def solveCube(self, maxIteration):
        print("Starting search process (Stochastic Hill-Climbing)")
        
        i = 0
        while i < maxIteration:
            neighbour = self.Node.getRandomSuccessor()

            if neighbour.current_value == 0:
                self.Node = neighbour
                self.history.append({"frame": i, "cube": self.Node.cube, "objective_value": self.Node.current_value})
                break

            if neighbour.current_value <= self.Node.current_value:
                neighbour2 = neighbour.getHighestSuccessor()
                if neighbour2.current_value <= self.Node.current_value:
                    self.Node = neighbour2
                else:
                    self.Node = neighbour

                print(f"Updated Node to new value: {self.Node.current_value}")

            self.history.append({"frame": i, "cube": self.Node.cube, "objective_value": self.Node.current_value})
            i += 1

        print(f"Initial state of the cube:")
        self.initial_state.showCube
        print(f"Final state of the cube:")
        self.Node.showCube()
        print(f"Final objective function value achieved: {self.Node.current_value}")
        print(f"Total iterations until search stopped: {i}")

        return self.Node
