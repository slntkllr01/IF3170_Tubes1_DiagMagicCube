import copy
from utils.node import Node

class Steepest:
    def __init__(self):
        self.Node = Node(cube_size=5)
        self.history = []  
        self.initial_state = copy.deepcopy(self.Node)
        self.history.append({
            "frame": 1,
            "cube": copy.deepcopy(self.Node.cube),
            "objective_value": self.Node.current_value
        })

    def solveCube(self):
        print("Starting search process (Steepest)")
        print(f"Initial Node(Objektif Value) value: {self.Node.current_value}")
        i = 2
        while True:
            neighbour = self.Node.getHighestSuccessor()

            if neighbour.current_value == 0:
                self.Node = neighbour
                self.history.append({"frame": i, "cube": copy.deepcopy(self.Node.cube),  "objective_value": self.Node.current_value})
                break

            if neighbour.current_value >= self.Node.current_value:
                print("Local maximum reached.")
                break

            self.Node = neighbour
            print(f"Updated Node(Objektif Value) to new value: {self.Node.current_value}")
            self.history.append({"frame": i, "cube": copy.deepcopy(self.Node.cube), "objective_value": self.Node.current_value})
            i += 1

        print(f"Initial state of the cube:")
        self.initial_state.showCube
        print(f"Final state of the cube:")
        self.Node.showCube()
        print(f"Final objective function value achieved: {self.Node.current_value}")
        print(f"Total iterations until search stopped: {i-1}")

        return self.Node
