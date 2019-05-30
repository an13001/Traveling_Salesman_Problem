from numpy import *
from random import *

MUTATION_RATE = 0.01
POPULATION_SIZE = 50
CITIES_NUMB = 25

# /////////////////////// Helping functions ///////////////////////////////

def find_element(List, a):
    for i in range(len(List)):
        if List[i] == a:
            return i
    return len(List) + 1

def swap(a,b):
    c = a
    a = b
    b = c

# ////////////////////////////////////////////////////////////////////////

"""
def initialize_map(distance_limit, nb_cities):
    _map = zeros((nb_cities,nb_cities))
    for i in range(nb_cities):
        for j in range(i):
            if random.random() > distance_limit:
                _map[i][j] = random.random()*1000
                _map[j][i] = _map[i][j]
            else:
                _map[i][j] = nb_cities*1000
                _map[j][i] = _map[i][j]                
    return _map
"""

class Population:
    def __init__(N, L):
        population = []
        for i in range(N):
            population += [suffle(L)]
        return population

class GA:
   def __init__(self, MUTATION_RATE, POPULATION_SIZE):
      self.mutation_rate = MUTATION_RATE
      self.population_size = POPULATION_SIZE

def distance(solution, Map):
    score = 0
    for i in range(1, len(route)):
        score = score + Map[solution[i-1]][solution[i]]
    return score  

def min_distance(selected_population, Map):
    solution = selected_population[0]
    for i in range(len(selected_population)):
        if(distance(solution, Map) < distance(selected_population[i], Map))
        solution = selected_population[i]
    return distance(solution, Map)

def fitness(solution, Map):
    return 1/float(distance(solution, Map))
    
def crossover(parent_1, parent_2):
    N = len(parent_1)
    for i in range(N):
        child_1.append(parent_1[i])
        child_2.append(parent_2[i])
    j = randint(1, N-1)
    # Creation of the first child
    index_1 = find_element(child_1, parent_2[j])
    swap(child_1[j], child_1[index_1])
    
    index_2 = find_element(child_1, parent_2[j-1])
    swap(child_1[j-1], child_1[index_2])

    index_3 = find_element(child_1, parent_2[j+1])
    swap(child_1[j+1], child_1[index_3])

    # creation of the second child
    index_1 = find_element(child_2, parent_1[j])
    swap(child_2[j], child_2[index_1])
    
    index_2 = find_element(child_2, parent_1[j-1])
    swap(child_2[j-1], child_2[index_2])
    
    index_3 = find_element(child_2, parent_1[j+1])
    swap(child_2[j+1], child_2[index_3])

    return [child_1, child_2]


def selection(population, Map):
    L = eye(CITIES_NUMB, POPULATION_SIZE/2)
    for i in range(POPULATION_SIZE/2):
        for j in range(i, POPULATION_SIZE):
            if(fitness(population[j], Map) > fitness(population[i], Map)):
                L[i] = population[j]
            else:
                L[i] = population[i]
    return L

def f(d, m):
    return 1/pow(float(d-0.99*m), 3)

def F(selected_population, Map):
    L = []
    m = min_distance(selected_population, Map)
    for i in range(len(selected_population)):
        d = distance(selected_population[i], Map)
        L += [f(d, m)]
    return L

# Correspond à la fonction de répartition on proba
def Roulette_Wheel(selected_population, Map):
    R = []
    L = F(selected_population, Map)
    # D global distance
    D = 0
    for i in range(len(L)):
        D += L[i]
    for i in range(len(L)):
        numerator = 0
        for j in range(i):
            numerator += L[j]
        R[i] = numerator / float(D)
    return R

def Roulette_index(R):
    x = random()
    if 0 <= x <= R[0]:
        return 0
    for i in range(len(R)-1):
        if R[i] < x <= R[i+1]:
return i+1
