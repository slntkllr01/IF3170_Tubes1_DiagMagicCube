from utils.node import Node
from utils.utility import Utility
from concurrent.futures import ThreadPoolExecutor
import statistics
import random

class GeneticAlgorithm:
    def __init__(self, cube_size, population_size, max_iterations):
        self.population = [Node(cube = None, cube_size = cube_size) for i in range (population_size)]
        self.population_size = population_size
        self.mutation_rate = 0.1
        self.max_iterations = max_iterations
        self.history = []
        self.mean_history = []

    def calculatePopulationFitness(self):
        result = []
        max_nodes = max(self.population).current_value

        for i in range (len(self.population)):
            result.append(max_nodes - self.population[i].calculateHeuristic())

        total = sum(result)

        if total == 0:
            return [1/self.population_size] * len(self.population)
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
        random_number = random.random()

        for i, (start, end) in enumerate(intervals):
            if start <= random_number < end:
                return self.population[i].cube

    def crossover(self, parent1, parent2):
        cutting_point_x = random.randint(0, 4)
        cutting_point_y = random.randint(0, 4)
        cutting_point_z = random.randint(0, 4)

        offspring1 = [[[0 for k in range (5)] for j in range (5)] for i in range (5)]
        offspring2 = [[[0 for k in range (5)] for j in range (5)] for i in range (5)]

        for i in range (5):
            for j in range (5):
                for k in range (5):
                    if (i < cutting_point_x) or (i == cutting_point_x and j < cutting_point_y) or (i == cutting_point_x and j == cutting_point_y and k <= cutting_point_z):
                        offspring1[i][j][k] = parent1[i][j][k]
                        offspring2[i][j][k] = parent2[i][j][k]
                    else:
                        offspring1[i][j][k] = parent2[i][j][k]
                        offspring2[i][j][k] = parent1[i][j][k]

        return offspring1, offspring2
    def mutation(self, offspring):
         Utility.swapElement(offspring)

    def createChild(self, fitness_scores):
        parent1 = self.selection()
        parent2 = self.selection()
        while (not parent1) or (not parent2):
            parent1 = self.selection()
            parent2 = self.selection()

        offspring1, offspring2 = self.crossover(parent1, parent2)

        if random.random() < self.mutation_rate:
            self.mutation(offspring1)
            self.mutation(offspring2)

        return offspring1, offspring2

    def solveGeneticAlgorithm(self):
        optimum_value = float('inf')
        for i in range (self.max_iterations):
            new_generation = []
            fitness_scores = self.calculatePopulationFitness()      

            with ThreadPoolExecutor(max_workers=20) as executor:
                for _ in range(self.population_size):
                    results = list(executor.map(lambda _: self.createChild(fitness_scores), range(self.population_size // 2)))
            
            for offspring1, offspring2 in results:
                new_generation.append(Node(offspring1))
                new_generation.append(Node(offspring2))

            best_individual = min(new_generation, key=lambda node: node.calculateHeuristic())
            mean_population = statistics.mean([node.calculateHeuristic() for node in new_generation])
            best_fitness = best_individual.calculateHeuristic()
            print(f"Generasi {i + 1}: Fitness terbaik = {best_fitness}")

            self.history.append({"frame": i + 1, "cube": best_individual.cube, "objective_value": best_fitness})
            self.mean_history.append({"frame": i + 1, "cube": best_individual.cube, "objective_value": mean_population})
            
            if best_fitness == 0:
                print("Solusi optimal ditemukan!")
                return best_individual
            
            self.population = new_generation

            if best_fitness < optimum_value:
                optimum_value = best_fitness

        print("Jumlah iterasi maksimum tercapai.")
        print("Maximum value: ", optimum_value)
        return best_individual
    