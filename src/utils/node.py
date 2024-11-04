from utils.utility import Utility
import random
import copy

class Node:
    def __init__(self, cube=None, cube_size=5):
        self.magic_number = Utility.magicNumber(cube_size)
        
        if cube is not None:
            self.cube = copy.deepcopy(cube)
        else:
            self.cube = Utility.generateRandomCube(cube_size, self.magic_number)

        self.current_value = Utility.objectiveFunction(self.cube, self.magic_number)
        self.mean = Utility.calculateMeanSums(self.cube)
        self.variance = Utility.calculateVarianceSums(self.cube)
        self.diff = Utility.differentValues(self.cube, self.magic_number)
    
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
        self.current_value = Utility.objectiveFunction(self.cube, self.magic_number)
        return self.current_value
    
    # buat cari sucessor paling oke
    def getHighestSuccessor(self):
        bestcube = None
        initcube = copy.deepcopy(self.cube)
        initval = Utility.objectiveFunction(initcube,315)
        value = self.current_value

        for i in range(125):
            for j in range(125):
                if i == j or i == 62 or j == 62:
                    continue

                newcube = copy.deepcopy(Utility.swapCubeValue(initcube, i, j))
                newval = Utility.objectiveFunction(newcube, 315)
              
                if newval < value and newval != initval:
                    value = newval
                    bestcube = copy.deepcopy(newcube)
                    
        newNode = Node(bestcube)
        return newNode
        
    # buat cari sucessor random kayak simulated dan stochastic
    def getRandomSuccessor(self):
        random1 = random.randint(0, 124)
        random2 = random.randint(0, 124)

        while random1==random2 or random1==62 or random2==62:
            random1 = random.randint(0, 124)
            random2 = random.randint(0, 124)

        newcube = copy.deepcopy(Utility.swapCubeValue(self.cube, random1, random2))

        while Utility.calculateMeanSums(newcube) > self.mean or Utility.calculateVarianceSums(newcube) > self.variance or Utility.differentValues(newcube,315) > self.diff:
            while random1==random2 or random1==62 or random2==62:
                random1 = random.randint(0, 124)
                random2 = random.randint(0, 124)
            newcube = copy.deepcopy(Utility.swapCubeValue(self.cube, random1, random2))

        newNode = Node(newcube)
        return newNode






        