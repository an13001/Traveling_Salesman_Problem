from math import *
import random
from matplotlib.pyplot import *

CITIES_NUMBER = 25
COLONY_SIZE = 10
Q = 1.0
RHO = 0.1
ALPHA = 1.0
BETA = 3.0
EXP_NUMB = 100
INITIAL_PHEROMONE=1.0
CITIES = [(random.uniform(-400, 400), random.uniform(-400, 400)) for _ in range(CITIES_NUMBER)]

# ////////////////////// Helping functions //////////////////////////////

def Roulette_Wheel(proba_list):
    R = []
    for i in range(len(proba_list)):
        counter = 0
        for j in range(i+1):
            counter += proba_list[j]
        R += [counter] 
    return R

# //////////////////////////////////////////////////////////////////////

class ACO_For_TSP:
    class Edges_Matrix:
        def _init_(self):       
            self.distances_matrix = []
            self.pheromone_matrix = []
    class Ant(Edges_Matrix):
        def _init_(self):
            self.tour  = []
            self.total_tour_distance = 0.0
            self.unvisited_cities = []
            for i in range(len(CITIES_NUMBER)):
                self.unvisitied_cities += [i]
            self.distances_matrix = []
            self.pheromone_matrix = []
            for i in range(CITIES_NUMBER):
                L1 = []
                L2 = []
                for j in range(CITIES_NUMBER):
                    L1 += [self.Distance(CITIES[i],CITIES[j])]
                    L2 += [INITIAL_PHEROMONE]
                self.distances_matrix += [L1]
                self.pheromone_matrix += [L2]
        def Distance(self,X1,X2):
            return sqrt(pow(X1[0]-X2[0], 2)+pow(X1[1]-X2[1], 2))
        def Roulette_Index(self,R):
            x = random.random()
            if 0 <= x <= R[0]:
                return self.unvisited_cities[0]
            for i in range(1,len(R)):
                if R[i-1] < x <= R[i]:
                    return self.unvisited_cities[i]
        def Total_Distance(self):
            self.total_tour_distance = 0.0
            for i in range(CITIES_NUMBER):
                self.total_tour_distance += self.distances_matrix[self.tour[i]][self.tour[(i+1) % CITIES_NUMBER]]
            return self.total_tour_distance
        def Pheromone_2_Add(self):
            for i in range(CITIES_NUMBER):
                self.pheromone_matrix[self.tour[i]][self.tour[(i+1) % CITIES_NUMBER]] += Q / self.total_tour_distance
        def Unvisited_Cities(self):
            self.unvisited_cities = []
            for city in range(CITIES_NUMBER):
                if city not in self.tour:
                    self.unvisited_cities += [city]
        def Creat_Proba_List(self):
            proba_list = []
            denomunator = 0.0
            self.Unvisited_Cities()
            for unvisited_city in self.unvisited_cities:
                denomunator += pow(self.distances_matrix[self.tour[-1]][unvisited_city], BETA) * \
                               pow(self.pheromone_matrix[self.tour[-1]][unvisited_city], ALPHA)
            for unvisited_city in self.unvisited_cities:
                numerator = pow(self.distances_matrix[self.tour[-1]][unvisited_city], BETA) * \
                            pow(self.pheromone_matrix[self.tour[-1]][unvisited_city], ALPHA)
                next_element = numerator / denomunator
                for i in range(len(proba_list)):
                    next_element += proba_list[i]
                proba_list += [next_element]
            return proba_list                    
        def Choose_Next_City(self):
            return self.Roulette_Index(Roulette_Wheel(self.Creat_Proba_List()))
        def Choose_Tour(self):
            self.tour = [random.randint(0, CITIES_NUMBER - 1)]
            while len(self.tour) < CITIES_NUMBER:
                self.tour.append(self.Choose_Next_City())
            return self.tour
        
    def __init__(self):
        self.Edges_Matrix.distances_matrix = []
        self.Edges_Matrix.pheromone_matrix = []
        for i in range(CITIES_NUMBER):
            L1 = []
            L2 = []
            for j in range(CITIES_NUMBER):
                L1 += [self.Distance(CITIES[i],CITIES[j])]
                L2 += [INITIAL_PHEROMONE]
            self.Edges_Matrix.distances_matrix += [L1]
            self.Edges_Matrix.pheromone_matrix += [L2]
        self.best_tour = [city for city in range(CITIES_NUMBER)]
        self.ants = [self.Ant() for _ in range(COLONY_SIZE)]
        for ant in self.ants:
            ant.tour = ant.Choose_Tour()
        self.best_distance = self.Total_Distance(self.best_tour) 

    def Total_Distance(self,tour):
        tour_length = 0.0
        for i in range(CITIES_NUMBER):
            tour_length += self.Edges_Matrix.distances_matrix[tour[i]][tour[(i+1) % CITIES_NUMBER]]
        return tour_length
    def Distance(self,X1,X2):
        return sqrt(pow(X1[0]-X2[0], 2)+pow(X1[1]-X2[1], 2))
    
    def Pheromone_2_Add(self, tour, total_tour_distance):
        for i in range(CITIES_NUMBER):
            self.Edges_Matrix.pheromone_matrix[tour[i]][tour[(i+1) % CITIES_NUMBER]] += Q / total_tour_distance
    def Aco(self):
        for i in range(EXP_NUMB):
            for ant in self.ants:
                ant.Choose_Tour()
                ant.Total_Distance()
                ant.Pheromone_2_Add()
                self.Pheromone_2_Add(ant.tour, ant.total_tour_distance)
                if ant.total_tour_distance < self.best_distance:
                    self.best_tour = ant.tour
                    self.best_distance = ant.total_tour_distance
            for i in range(CITIES_NUMBER):
                for j in range(CITIES_NUMBER):
                    self.Edges_Matrix.pheromone_matrix[i][j] *= (1.0 - RHO)
            for ant in self.ants:
                for i in range(CITIES_NUMBER):
                    for j in range(CITIES_NUMBER):
                        ant.pheromone_matrix[i][j] *= (1.0 - RHO)
    def Plot(self):
        x = [CITIES[i][0] for i in self.best_tour]
        x.append(x[0])
        y = [CITIES[i][1] for i in self.best_tour]
        y.append(y[0])
        print(self.best_tour)
        plot(x, y)
        show()
    
        
if __name__ == '__main__':
    aco = ACO_For_TSP()
    aco.Aco()
    aco.Plot()
