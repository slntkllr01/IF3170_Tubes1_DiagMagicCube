from utils.node import Node
from utils.utility import Utility
from concurrent.futures import ThreadPoolExecutor
import random

class GeneticAlgorithm:
    def __init__(self, cube_size, population_size, max_iterations):
        self.population = [Node(cube_size = cube_size) for i in range (population_size)]
        self.population_size = population_size
        self.mutation_rate = 0.1
        self.max_iterations = max_iterations

    def calculatePopulationFitness(self):
        result = [0 for i in range (len(self.population))]
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

        for i in range (len(population_fitness) - 1):
            start = temp
            temp += population_fitness[i]
            intervals.append((start, temp))

        return intervals

    def selection(self):
        intervals = self.createInterval()
        random_number = random.randint(0, 1)

        for i, (start, end) in enumerate(intervals):
            if start <= random_number < end:
                return self.population[i].cube

    def crossover(parent1, parent2):
        cutting_point_x = random.randint(0, 4)
        cutting_point_y = random.randint(0, 4)
        cutting_point_z = random.randint(0, 4)

        offspring1 = [[[0 for k in range (5)] for j in range (5)] for i in range (5)]
        offspring2 = [[[0 for k in range (5)] for j in range (5)] for i in range (5)]

        for i in range (5):
            for j in range (5):
                for k in range (5):
                    if (i < cutting_point_x) or (i == cutting_point_x and j < cutting_point_y) or (i == cutting_point_x and j == cutting_point_y and k <= cutting_point_z):
                        offspring1[i][j][k] = parent1.cube[i][j][k]
                        offspring2[i][j][k] = parent2.cube[i][j][k]
                    else:
                        offspring1[i][j][k] = parent2.cube[i][j][k]
                        offspring2[i][j][k] = parent1.cube[i][j][k]

        return offspring1, offspring2
    def mutation(offspring):
         Utility.swapCubeValue(offspring)

    def createChild(self, fitness_scores):
        parent1 = self.selection()
        parent2 = self.selection()

        offspring1, offspring2 = self.crossover(parent1, parent2)

        if random.randint(0, 1) < self.mutation_rate:
            self.mutation(offspring1)
            self.mutation(offspring2)

        return offspring1, offspring2

    def solveGeneticAlgorithm(self):
        for i in range (self.max_iterations):
            new_generation = []
            fitness_scores = self.calculatePopulationFitness()

            with ThreadPoolExecutor(max_workers=5) as executor:
                for _ in range(self.population_size):
                    results = list(executor.map(self.createChild(fitness_scores), range(self.population_size // 2)))
            
            for offspring1, offspring2 in results:
                new_generation.append(Node(offspring1))
                new_generation.append(Node(offspring2))

            self.population = new_generation

            best_individual = max(self.population, key=lambda node: node.calculateHeuristic())
            best_fitness = best_individual.calculateHeuristic()

            print(f"Generasi {i + 1}: Fitness terbaik = {best_fitness}")

            if best_fitness == max(self.population).current_value:  # Misalnya, kondisi optimal tercapai
                print("Solusi optimal ditemukan!")
                return best_individual
            
        print("Jumlah iterasi maksimum tercapai.")
        return best_individual
    
# genetic_algorithm = GeneticAlgorithm(5, 20, 100)
# best_individual = genetic_algorithm.solveGeneticAlgorithm()

# print(best_individual.getCube())