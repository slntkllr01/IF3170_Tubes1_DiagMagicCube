from utils.node import Node

# masih jelek baru basicnya aja belum dikembangin
class Stochastic:
    def __init__(self):
        self.Node = Node(cube_size=5)

    def solveCube(self, maxIteration):
        i = 0
        while i < maxIteration:
            neighbour = self.Node.getRandomSuccessor()
            if neighbour.current_value <=  self.Node.current_value :
                self.Node = neighbour
                print(neighbour.current_value)
            else:
                i+=1

        return self.Node