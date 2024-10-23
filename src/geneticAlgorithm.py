from utils import *

class GeneticAlgorithm:
    def __init__(self, cube_size, population_size):
        self.population = [Node(cube_size) for i in range (population_size)]

    def calculatePopulationFitness(self):
        result = []

        max_nodes = max(self.population).current_value

        for i in range (len(self.population)):
            result.append(max_nodes - self.population[i].calculateHeuristic())

        total = sum(result)

        for i in range (len(self.population)):
            temp = result[i]
            result[i] = temp / total

        return result
    
    def createInterval(self):
        population_fitness = self.calculatePopulationFitness()
        intervals = []
        temp = 0

        for i in range (len(population_fitness)-1):
            start = temp
            temp += population_fitness[i]
            intervals.append((start, temp))

        return intervals

    def selection(self):
        intervals = self.createInterval()
        random_number = random.randint(0, 1)

        for i, (start, end) in enumerate(intervals):
            if start <= random_number < end:
                return self.population[i]


    def crossover(self, other):
        cuttingpoint = random.randint(1, len(self.cube) - 2)

        offspring1 = self.population[:cuttingpoint] + other.population[cuttingpoint:]
        offspring2 = other.population[:cuttingpoint] + self.population[cuttingpoint:]

        return offspring1, offspring2
    
    def mutation(self):
        for i in range (len(self.population)):
            Utility.swapElement(self.population[i].getCube())
        
# test = GeneticAlgorithm(3, 5)

# print(test.calculatePopulationFitness())

# print(test.createInterval())

        
    

    


        

            




