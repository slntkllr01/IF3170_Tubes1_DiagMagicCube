from utils.node import Node

class Stochastic:
    def __init__(self):
        self.Node = Node(cube_size=5)
        self.history = []  

    def solveCube(self, maxIteration):
        i = 0
        while i < maxIteration:
            neighbour = self.Node.getRandomSuccessor()

            if neighbour.current_value == 0:
                self.Node = neighbour
                self.history.append(self.Node)  
                break

            if neighbour.current_value <= self.Node.current_value:

                neighbour2 = neighbour.getHighestSuccessor()
                if neighbour2.current_value <= self.Node.current_value:
                    self.Node = neighbour2
                else:
                    self.Node = neighbour

                self.history.append(self.Node)

                print(f"Updated Node to new value: {self.Node.current_value}")

            i += 1

        return self.Node
