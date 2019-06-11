import random
from scipy import *
from matplotlib.pyplot import *
CITIES_NUMBER = 20
T0 = 10.0
Tmin = 1e-2
tau = 1e4
# //////////////////// Helping Functions //////////////////////////////
def swap(i,j):
    global Final_Tour
    c = Final_Tour[j]
    Final_Tour[j] = Final_Tour[i]
    Final_Tour[i] = c
def Generate_Rand_List(n):
    L = []
    for i in range(n):
        L += [random.random()]
    return L
# //////////////////////////////////////////////////////////////////////
X = Generate_Rand_List(CITIES_NUMBER)
Y = Generate_Rand_List(CITIES_NUMBER)
 
Init_Tour = arange(CITIES_NUMBER)
Final_Tour = arange(CITIES_NUMBER)

def Tour_Energy():
    global Final_Tour
    energy = 0.0
    for i in range(len(Final_Tour)):
        energy += sqrt((X[Final_Tour[i]]-X[Final_Tour[(i+1) % len(Final_Tour)]])**2 + \
                       (Y[Final_Tour[i]]-Y[Final_Tour[(i+1) % len(Final_Tour)]])**2)
    return energy

def Fluctuation(i,j):
    global Final_Tour
    swap(i,j)
    
def Metropolis(E1,E2,T,i,j):
    if E1 <= E2:
        E2 = E1
    else:
        dE = E1-E2
        if random.uniform() > exp(-dE/T): 
            Fluctuation(i,j)              
        else:
            E2 = E1 
    return E2

def Run():
    init_energy = Tour_Energy()
    t = 0
    T = T0
    while T > Tmin:
        i = random.random_integers(0,CITIES_NUMBER-1)
        j = random.random_integers(0,CITIES_NUMBER-1)
        while i == j:
            i = random.random_integers(0,CITIES_NUMBER-1)
        Fluctuation(i,j)
        final_energy = Tour_Energy()   
        init_energy = Metropolis(final_energy,init_energy,T,i,j)
        t += 1
        # refresh the system
        T = T0*exp(-t/tau)
    final_x =[]
    final_y =[]
    init_x =[]
    init_y =[]
    for i in range(len(Final_Tour)):
        init_x += [X[Init_Tour[i]]]
        init_y += [Y[Init_Tour[i]]]
        final_x += [X[Final_Tour[i]]]
        final_y += [Y[Final_Tour[i]]]
    init_x += [X[Init_Tour[0]]]
    init_y += [Y[Init_Tour[0]]]
    final_x += [X[Final_Tour[0]]]
    final_y += [Y[Final_Tour[0]]]
    subplot(1, 2, 1)
    plot(final_x,final_y,'k')
    plot(X,Y, 'ro')
    title('Initial Tour')
    subplot(1, 2, 2)
    plot(init_x,init_y,'k')
    plot(X,Y, 'ro')
    title('Optimal tour')
    show()
Run()
