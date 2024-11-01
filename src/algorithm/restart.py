from utils.node import Node

class RandomRestart:
    def __init__(self):
        pass

    def solveCube(self, maxRestart):
        currvalue = float('inf')
        currcube = None

        for i in range(maxRestart):
            RandomNode = Node(cube_size=5)
            
            while True:
                neighbour = RandomNode.getHighestSuccessor()

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
                print(f"New best value found: {currvalue}")

        return currcube
