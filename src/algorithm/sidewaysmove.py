import copy
from utils.node import Node

class SidewaysMove:
    def __init__(self):
        self.Node = Node(cube_size=5)
        self.history = []  
        self.initial_state = copy.deepcopy(self.Node)
        self.history.append({
            "frame": 1,
            "cube": copy.deepcopy(self.Node.cube),
            "objective_value": self.Node.current_value
        })

    def solveCube(self, max_sideways_moves):
        print("Starting search process (Sideways Move Hill-Climbing)")
        
        i = 2
        sideways_moves = 0
        print(f"Initial Node(Objektif Value) value: {self.Node.current_value}")
        while sideways_moves<max_sideways_moves:
            neighbour = self.Node.getHighestSuccessor()
            print(f"neighbor value : {neighbour.current_value}     current value : {self.Node.current_value} ")

            if neighbour.current_value == 0:
                self.Node = neighbour
                self.history.append({"frame": i, "cube": copy.deepcopy(self.Node.cube),  "objective_value": self.Node.current_value})
                break

            if neighbour.current_value > self.Node.current_value:
                print("Local maximum reached.")
                break
            
            if neighbour.current_value <= self.Node.current_value:
                self.Node = neighbour

            if neighbour.current_value == self.Node.current_value:
                sideways_moves += 1

            print(f"Updated Node(Objektif Function) to new value: {self.Node.current_value}")
            self.history.append({"frame": i, "cube": copy.deepcopy(self.Node.cube),  "objective_value": self.Node.current_value})
            i += 1

        print(f"Initial state of the cube:")
        self.initial_state.showCube
        print(f"Final state of the cube:")
        self.Node.showCube()
        print(f"Final objective function value achieved: {self.Node.current_value}")
        print(f"Total iterations until search stopped: {i-1}")
        print(f"Total sideways move: {sideways_moves}")

        return self.Node
