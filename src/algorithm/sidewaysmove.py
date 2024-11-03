import copy
from utils.node import Node

class SidewaysMove:
    def __init__(self):
        self.Node = Node(cube_size=5)
        self.history = []  
        self.initial_state = copy.deepcopy(self.Node)
        self.history.append({
            "frame": 0,
            "cube": copy.deepcopy(self.Node.cube),
            "objective_value": self.Node.current_value
        })

    def solveCube(self, max_sideways_moves):
        print("Starting search process (Sideways Move Hill-Climbing)")
        
        i = 1
        sideways_moves = 0

        while True:
            neighbour = self.Node.getHighestSuccessor()
            print(f"neighbor value : {neighbour.current_value}     current value : {self.Node.current_value} ")

            if neighbour.current_value < self.Node.current_value:
                print("Local maximum reached.")
                break
            
            if neighbour.current_value > self.Node.current_value:
                self.Node = neighbour

            elif neighbour.current_value == self.Node.current_value:
                if sideways_moves < max_sideways_moves:
                    sideways_moves += 1
                    self.Node = neighbour
                else:
                    print("Max sideways moves reached. Stopping search.")
                    break

            self.history.append({"frame": i, "cube": copy.deepcopy(self.Node.cube),  "objective_value": self.Node.current_value})
            print(f"Updated Node to new value: {self.Node.current_value}")
            i += 1

        print(f"Initial state of the cube:")
        self.initial_state.showCube
        print(f"Final state of the cube:")
        self.Node.showCube()
        print(f"Final objective function value achieved: {self.Node.current_value}")
        print(f"Total iterations until search stopped: {i}")
        print(f"Total sideways move: {sideways_moves}")

        return self.Node
