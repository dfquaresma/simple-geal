import math
import random
import statistics 

class Gene:
  def __init__(self, x):
        self._x = x

  @property
  def x(self):
      return self._x

def first_population(population_size, abscissa_interval):
  population = population_size * [0]
  for i in range(0, population_size):
    population[i] = Gene(random.uniform(abscissa_interval[0], abscissa_interval[1]))
  
  return population

def mutation(gene):
  return Gene(gene.x + random.random() - random.random())

def fit_function(gene):
  x = gene.x
  return -(math.sin(x**3) + math.atan(x**7) + math.cosh(x))

def crossover(gene1, gene2):
  part1 = random.random()
  part2 = 1 - part1
  return Gene(gene1.x * part1 + gene2.x * part2)

def standard_deviation(population):
  x_values = []
  for gene in population:
    x_values.append(gene.x)
  return statistics.stdev(x_values)

def generate(population, max_generation_number, minimum_sd, mutation_rate, crossover_size):
  for i in range(max_generation_number):
    if standard_deviation(population) >= minimum_sd:
      break

    # Apply mutation on each gene
    for i in range(len(population)):
      if random.random() >= mutation_rate:
        population[i] = mutation(population[i]) 
    
    start_crossover = len(population) - crossover_size

    # Generate new genes from the best existing genes
    new_generation = []
    population = sorted(population, key = fit_function)
    for i in range(start_crossover, len(population)):
      for j in range(start_crossover, len(population)):
        new_generation.append(crossover(population[i], population[j]))

    # Replace old wrost genes  
    new_generation = sorted(new_generation, key = fit_function, reverse=True)
    for i in range(start_crossover):
      if fit_function(population[i].x) < fit_function(new_generation[i].x): 
        population[i] = new_generation[i]    

  return population

if __name__ == '__main__':
  abscissa_interval = tuple(map(float, input("The min and max values for x: ").split()))
  max_generation_number = int(input("Max number of generations: "))
  population_size = int(input("Population size: "))
  minimum_sd = float(input("Minimum acceptable standard deviation: ")) 
  mutation_rate = float(input("A probability between 0 and 1 of each gene mutation: "))
  crossover_size = int(input("The number of genes to crossover: "))

  population = first_population(population_size, abscissa_interval)
  genes = generate(population, max_generation_number, minimum_sd, mutation_rate, crossover_size)
  
  print("Best solution found is:", end=" ")
  print(max(genes, key=fit_function).x, ", and true best solution is -1.177278297688")
  