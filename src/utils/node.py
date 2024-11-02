from utils.utility import Utility
import random

class Node:
    def __init__(self, cube=None, cube_size=5):
        self.magic_number = Utility.magicNumber(cube_size)
        
        if cube is not None:
            self.cube = cube
        else:
            self.cube = Utility.generateRandomCube(cube_size, self.magic_number // 2)

        self.current_value = Utility.heuristicFunction(self.cube, self.magic_number)
    
    def __eq__(self, other):
        return self.current_value == other.current_value
    
    def __lt__(self, other):
        return self.current_value < other.current_value
    
    def __gt__(self, other):
        return self.current_value > other.current_value
    
    def getCube(self):
        return self.cube
    
    def getElement(self, i, j, k):
        return self.cube[i][j][k]
    
    def getCubeSize(self):
        return self.cube_size
    
    def showCube(self):
        for i in range (len(self.cube)):
            for j in range (len(self.cube)):
                for k in range (len(self.cube)):
                    print(self.cube[i][j][k], end=' ')
                print()
            print()

    def calculateHeuristic(self):
        self.current_value = Utility.heuristicFunction(self.cube, self.magic_number)
        return self.current_value
    
    # buat cari sucessor paling oke
    def getHighestSuccessor(self):
        bestcube = self.cube
        value = self.current_value

        for i in range (125):
            for j in range (125):
                if i==j or i==62 or j==62:
                    continue
                newcube = Utility.swapCubeValue(self.cube, i, j)
                newval = Utility.heuristicFunction(self.cube, 315)

                if newval < value:
                    value = newval
                    bestcube = newcube

        newNode = Node(bestcube)
        return newNode
    
    # buat cari sucessor random kayak simulated dan stochastic
    def getRandomSuccessor(self):
        random1 = random.randint(0, 124)
        random2 = random.randint(0, 124)

        while random1==random2 or random1==62 or random2==62:
            random1 = random.randint(0, 124)
            random2 = random.randint(0, 124)

        newcube = Utility.swapCubeValue(self.cube, random1, random2)

        newNode = Node(newcube)
        return newNode






        