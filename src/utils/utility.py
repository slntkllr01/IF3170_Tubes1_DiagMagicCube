import random

class Utility:
    def __init__(self):
        pass

    @staticmethod
    def magicNumber(cube_size):
        return (cube_size * (cube_size**3 + 1)) / 2
    
    @staticmethod
    def objectiveFunction(cube, magic_number):
        obejective_cost = 0
        n = 5

        main_diagonal_1 = 0
        main_diagonal_2 = 0
        diagonal_ltr = 0
        diagonal_rtl = 0
        diagonal_ttb = 0
        diagonal_btt = 0

        for i in range(n):
            for j in range(n):
                row_sum = 0
                col_sum = 0
                pillar_sum = 0
                for k in range(n):
                    row_sum += cube[i][j][k]
                    col_sum += cube[i][k][j]
                    pillar_sum += cube[k][i][j]

                obejective_cost += abs(row_sum - magic_number)
                obejective_cost += abs(col_sum - magic_number)
                obejective_cost += abs(pillar_sum - magic_number)

            main_diagonal_1 += cube[i][i][i]
            main_diagonal_2 += cube[i][i][n - i - 1]
            diagonal_ltr += cube[i][n - i - 1][i]
            diagonal_rtl += cube[n - i - 1][i][i]
            diagonal_ttb += cube[i][i][i]
            diagonal_btt += cube[n - i - 1][i][i]

        obejective_cost += abs(main_diagonal_1 - magic_number)
        obejective_cost += abs(main_diagonal_2 - magic_number)
        obejective_cost += abs(diagonal_ltr - magic_number)
        obejective_cost += abs(diagonal_rtl - magic_number)
        obejective_cost += abs(diagonal_ttb - magic_number)
        obejective_cost += abs(diagonal_btt - magic_number)

        return obejective_cost

    @staticmethod
    def generateRandomCube(cube_size, magic_number):
        cube = Utility.RandomCube(cube_size,magic_number)

        while not Utility.eliminateRandomState(cube):
            cube = Utility.RandomCube(cube_size,magic_number)

        return cube
    
    def RandomCube(cube_size, magic_number):
        cube = [[[0 for k in range (cube_size)] for j in range (cube_size)] for i in range (cube_size)]
        num = [i for i in range(1,126)]
        num.remove(63) # hapus 63 karena nanti gak masuk random

        for i in range (cube_size):
            for j in range (cube_size):
                for k in range (cube_size):
                    if i==2 and j==2 and k==2:
                        cube[i][j][k] = 63
                    else:
                        randomidx= random.randint(0, len(num)-1)
                        randomnum = num[randomidx]
                        num.pop(randomidx)
                        cube[i][j][k] = randomnum

        return cube
    
    @staticmethod
    def swapElement(cube):
        i1, j1, k1 = random.randint(0, len(cube)-1), random.randint(0, len(cube)-1), random.randint(0, len(cube)-1)
        i2, j2, k2 = random.randint(0, len(cube)-1), random.randint(0, len(cube)-1), random.randint(0, len(cube)-1)
        
        cube[i1][j1][k1], cube[i2][j2][k2] = cube[i2][j2][k2], cube[i1][j1][k1]
        
    @staticmethod
    # tukar dua angka di dalam cube
    def swapCubeValue(cube, pos1, pos2):
        cubetemp = cube

        i1, j1, k1 = Utility.postoijk(pos1)
        i2, j2, k2 = Utility.postoijk(pos2)

        while (i1==2 and j1==2 and k1==2) or (i1==i2 and j1==j2 and k1==k2):
            i1, j1, k1 = Utility.postoijk(pos1)
        while (i2==2 and j2==2 and k2==2) :
            i1, j1, k1 = Utility.postoijk(pos2)

        # tukar posisi angka
        temp = cubetemp[i1][j1][k1]
        cubetemp[i1][j1][k1] = cubetemp[i2][j2][k2]
        cubetemp[i2][j2][k2] = temp

        return cubetemp
    
    def postoijk(pos):
        i1 = pos//25
        j1 = (pos%25)//5
        k1 = (pos%25)%5

        return i1,j1,k1
    
    def eliminateRandomState(cube):
        if cube[2][2][0] + cube[2][4][4] == 126 or cube[2][2][0] + cube[2][2][4] == 126 or cube[2][0][2] + cube[2][4][2] == 126 or cube[2][0][4] + cube[2][4][0] == 126 :
            return True
        return False



