from utils.node import Node

class SidewaysMove:
    def __init__(self):
        self.Node = Node(cube_size=5)
        self.history = []  
        self.initial_state = self.Node

    def solveCube(self, maxIteration):
        print("Starting search process (Sideways Move Hill-Climbing)")
        
        i = 0
        sideways_moves = 0
        max_sideways_moves = 2

        while i < maxIteration:
            neighbour = self.Node.getHighestSuccessor()

            if neighbour.current_value < self.Node.current_value:
                print("Local maximum reached.")
                break
            
            if neighbour.current_value > self.Node.current_value:
                self.Node = neighbour
                sideways_moves = 0 

            elif neighbour.current_value == self.Node.current_value:
                if sideways_moves < max_sideways_moves:
                    sideways_moves += 1
                    self.Node = neighbour
                    print(f"Performed a sideways move (count: {sideways_moves})")
                else:
                    print("Max sideways moves reached. Stopping search.")
                    break

            # Log and increment iteration
            self.history.append({"frame": i, "cube": self.Node.cube, "objective_value": self.Node.current_value})
            print(f"Updated Node to new value: {self.Node.current_value}")
            i += 1

        print(f"Initial state of the cube:")
        self.initial_state.showCube
        print(f"Final state of the cube:")
        self.Node.showCube()
        print(f"Final objective function value achieved: {self.Node.current_value}")
        print(f"Total iterations until search stopped: {i}")

        return self.Node
