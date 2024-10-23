from utils.node import Node

# masih jelek baru basicnya aja belum dikembangin
class RandomRestart:
    def __init__(self):
        pass

    def solveCube(self, maxRestart):
        currvalue = 999999999
        currcube = None

        for i in range(maxRestart):
            RandomNode = Node(cube_size=5)
            while (True):
                neighbour = RandomNode.getHighestSuccessor()
                if neighbour.current_value <=  RandomNode.current_value :
                    RandomNode = neighbour
                else:
                    break
                print(RandomNode.current_value)

            if RandomNode.current_value < currvalue :
                currvalue = RandomNode.current_value
                currcube = RandomNode

        print(currvalue)
        return currcube




