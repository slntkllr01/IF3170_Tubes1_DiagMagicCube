import random

class Utility:
    def __init__(self):
        pass

    @staticmethod
    def magicNumber(cube_size):
        return (cube_size * (cube_size**3 + 1)) / 2
    
    @staticmethod
    def heuristicFunction(cube, magic_number):
    
        heuristic_cost = 0

        # assume layer = i, row = j, column = k
        # cek semua baris, kolom, dan pilar di setiap layer
        for i in range (len(cube)):
            sum_main_diagonal_1 = 0
            sum_main_diagonal_2 = 0
            sum_diagonal_ltr = 0
            sum_diagonal_rtl = 0
            sum_diagonal_ttb = 0
            sum_diagonal_btt = 0
            for j in range (len(cube)):
                sum_row = 0
                sum_col = 0
                sum_pilar = 0
                for k in range (len(cube)):
                    sum_row += cube[j][k][i]
                    sum_col += cube[i][k][j]
                    sum_pilar += cube[k][i][j]
                heuristic_cost += (
                    abs(sum_row - magic_number) +
                    abs(sum_col - magic_number) +
                    abs(sum_pilar - magic_number))
                
                sum_main_diagonal_1 += cube[j][j][i]
                sum_main_diagonal_2 += cube[j][len(cube)-j-1][i]
                sum_diagonal_ltr += cube[j][i][j]
                sum_diagonal_rtl += cube[j][len(cube)-j-1][j]
                sum_diagonal_ttb += cube[i][j][j]
                sum_diagonal_btt += cube[len(cube)-1-j][j][j]
            heuristic_cost += (
                abs(sum_main_diagonal_1 - magic_number) + 
                abs(sum_main_diagonal_2 - magic_number) + 
                abs(sum_diagonal_rtl - magic_number) + 
                abs(sum_diagonal_ltr - magic_number) + 
                abs(sum_diagonal_ttb - magic_number) + 
                abs(sum_diagonal_btt - magic_number)
            )
        
        return heuristic_cost
    
    @staticmethod
    def generateRandomCube(cube_size, magic_number):
        cube = [[[0 for k in range (cube_size)] for j in range (cube_size)] for i in range (cube_size)]

        for i in range (cube_size):
            for j in range (cube_size):
                for k in range (cube_size):
                    cube[i][j][k] = random.randint(1, magic_number)

        return cube
    
    @staticmethod
    def swapElement(cube):
        i1, j1, k1 = random.randint(0, len(cube)-1), random.randint(0, len(cube)-1), random.randint(0, len(cube)-1)
        i2, j2, k2 = random.randint(0, len(cube)-1), random.randint(0, len(cube)-1), random.randint(0, len(cube)-1)
        
        cube[i1][j1][k1], cube[i2][j2][k2] = cube[i2][j2][k2], cube[i1][j1][k1]
    
class Node:
    def __init__(self, cube_size):
        self.magic_number = Utility.magicNumber(cube_size)
        self.cube = Utility.generateRandomCube(cube_size, self.magic_number//2)
        self.cube_size = cube_size
        self.current_value = 0
    
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