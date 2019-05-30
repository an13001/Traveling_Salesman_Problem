class Ant:
    def __init__(self, alpha, beta, num_nodes, edges):
            self.alpha = alpha
            self.beta = beta
            self.num_nodes = num_nodes
            #self.edges = edges
            self.Tour = None
            self.distance = 0.0

class Cities_Graph:
    def __init(self, Ligne: list, colonne: list, distance: list, visibility: list, pheromone_value: list):
        self.Ligne = Ligne
        self.colonne = colonne
        self.distance = distance
        self.visibility = visibility
        self.pheromone_value = pheromone_value

class ACO:
    ants_per_city = []
    nb_ants = 100
    nb_cities = 40
    rho = 0.5
    Q = 100

    def __init__(self, ants_per_city, ants_list, c):
        self.ants_per_city = ants_per_city
        self.ants_list = ants_list
        for i in range(len(self.ants_list)):
            # initialise self.ants_list[i].Tour
            for i in range(len(self.graph.Ligne)):
                self.graph.pheromone_value[i] = c
    
    def Choose_next_city(Nu, i, j, To, Ant_k):
        for k in range(Ant_k.num_nodes):
            if j == Ant_k.Tour[k]:
                print("This city has already been visited !")
                return 0
        Sum = 0
        for k in range(Ant_k.num_nodes):
            Sum += pow(T[i][Ant_k.Tour[k]], Ant_k.alpha)*pow(Nu[i][Ant_k.Tour[k]], Ant_k.beta)
        Prod = pow(T[i][j], Ant_k.alpha)*pow(Nu[i][j], Ant_k.beta)
        return Prod/Sum

    def Update_pheromone(Ant_k, graph, self, i, j):
        for k in range(len(graph.Ligne)):
            if i == Ligne[k] and j == colonne[k]:
                pheromone_value[k] = self.rho*pheromone_value[i] + self.Q/Ant_k.distance
                break

    def Solve_TSP(self):
        for i in range(nb_cities):
            # get ants from a city to another untill they get back to their starts
        #choose the best solution and continue
