from numpy import *
from random import *
from matplotlib.pyplot import *

MUTATION_RATE = 0.01
POPULATION_SIZE = 50
ELITE_SIZE = 10
CITIES_NUMBER = 25
GENERATIONS_NUMBER = 200

# /////////////////////// Helping functions ///////////////////////////////

def find_element_index(List, a):
    for i in range(len(List)):
        if List[i] == a:
            return i
    return -1

def swap(L,i,j):
    c = L[i]
    L[i] = L[j]
    L[j] = c 

def Generate_Rand_List(n):
    L = []
    for i in range(n):
        L += [random()]
    return L

# ////////////////////////////////////////////////////////////////////////

X = Generate_Rand_List(CITIES_NUMBER)
Y = Generate_Rand_List(CITIES_NUMBER)

def Create_Individual():
    L = []
    for i in range(CITIES_NUMBER):
        L += [i]
    individual = sample(L, CITIES_NUMBER)
    return individual

def Create_Population():
    L = []
    for i in range(POPULATION_SIZE):
        L += [Create_Individual()]
    return L

def Tour_Length(individual):
    score = 0
    for i in range(len(individual)):
        score += sqrt((X[individual[i]]-X[individual[(i+1) % len(individual)]])**2 + \
                       (Y[individual[i]]-Y[individual[(i+1) % len(individual)]])**2)
    return score  

def Min_Length(selected_population):
    best_individual = selected_population[0]
    for i in range(len(selected_population)):
        if(Tour_Length(best_individual) < Tour_Length(selected_population[i])):
            best_individual = selected_population[i]
    return Tour_Length(best_individual)

def Best_Individual_Index(selected_population):
    i = 0    
    for j in range(len(selected_population)):
        if(Tour_Length(selected_population[i]) < Tour_Length(selected_population[j])):
            i = j
    return i

def Crossover(parent_1, parent_2):
    N = len(parent_1)
    child_1 = []
    child_2 = []
    help_1 = []
    help_2 = []
    for k in range(N):
        child_1 += [parent_1[k]]
        child_2 += [parent_2[k]]
        help_1 += [parent_1[k]]
        help_2 += [parent_2[k]]
    i = randint(0, N-2) 
    j = randint(i+1,N-1)
    # exchange of genes
    for k in range(i,j+1):
        child_1[k] = parent_2[k]
        child_2[k] = parent_1[k]
        help_1[k] = -1
        help_2[k] = -1
    # Correction of the genetic code of the children
    for k in range(i,j+1):
        # correction of the first child
        if find_element_index(help_1, parent_2[k]) != -1 :
            index_1 = find_element_index(help_1, parent_2[k])
            child_1[index_1] = parent_1[k]
        # correction of the second child
        if find_element_index(help_2, parent_1[k]) != -1 :
            index_2 = find_element_index(help_2, parent_1[k])
            child_2[index_2] = parent_2[k]
    return [child_1,child_2]

def Selection(population):
    L = []
    for i in range(POPULATION_SIZE):
        L += [population[i]]
    for i in range(ELITE_SIZE):
        swap(L,i,Best_Individual_Index(L[i:POPULATION_SIZE]))
    return L[0:ELITE_SIZE]

def f(d, m):
    return 1/pow(float(d-0.99*m), 3)

def Fitness_Array(selected_population):
    L = []
    m = Min_Length(selected_population)
    for i in range(len(selected_population)):
        d = Tour_Length(selected_population[i])
        L += [f(d, m)]
    return L


def Roulette_Wheel(selected_population):
    R = []
    L = Fitness_Array(selected_population)
    # D is the global distance
    D = 0
    for i in range(len(L)):
        D += L[i]
    for i in range(len(L)):
        numerator = 0
        for j in range(i+1):
            numerator += L[j]
        R += [numerator / float(D)]
    return R

def Roulette_index(R):
    x = random()
    if 0 <= x <= R[0]:
        return 0
    for i in range(1,len(R)):
        if R[i-1] < x <= R[i]:
            return i

def mutation(individual):
    for i in range(len(individual)-1):
        if(random() < MUTATION_RATE):
            j = randint(i+1,len(individual)-1)
            L = []
            for k in range(i):
                L += [individual[k]]
            for k in range(j,i-1,-1):
                L += [individual[k]]
            for k in range(j+1,len(individual)):
                L += [individual[k]]
            return L
    return individual


def Next_Generation(population):
    L = []
    L += Selection(population)
    help_list = []
    for k in range((len(population)-ELITE_SIZE)/2):
        i = Roulette_index(Roulette_Wheel(population))
        j = Roulette_index(Roulette_Wheel(population))
        help_list += Crossover(population[i],population[j]) 
        L += [mutation(help_list[0]),mutation(help_list[1])]
    return L
    
def Genetic_Algorithm():
    population = Create_Population()
    for i in range(GENERATIONS_NUMBER):
        population = Next_Generation(population)
    return population[Best_Individual_Index(population)] 

def Plot():
    best_individual = Genetic_Algorithm()
    init_individual = []
    for i in range(len(best_individual)):
        init_individual += [i]
    final_x =[]
    final_y =[]
    init_x =[]
    init_y =[]
    for i in range(len(best_individual)):
        init_x += [X[init_individual[i]]]
        init_y += [Y[init_individual[i]]]
        final_x += [X[best_individual[i]]]
        final_y += [Y[best_individual[i]]]
    init_x += [X[init_individual[0]]]
    init_y += [Y[init_individual[0]]]
    final_x += [X[best_individual[0]]]
    final_y += [Y[best_individual[0]]]
    subplot(1, 2, 1)
    plot(final_x,final_y,'k')
    plot(X,Y, 'ro')
    title('Initial Tour')
    subplot(1, 2, 2)
    plot(init_x,init_y,'k')
    plot(X,Y, 'ro')
    title('Optimal tour')
    show()
Plot()
