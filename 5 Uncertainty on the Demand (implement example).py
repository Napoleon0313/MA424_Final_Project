from gurobipy import *
import numpy as np
import pandas as pd

# Parameters
T = 10 # demand uncertainty happens in the following 10 months
N = 3 # 3 different products

# assume price of each product in the following months follows 
# the uniform distribution between 5 and 10
np.random.seed(10)
p = np.random.uniform(5,10,size = [T,N])

# assume cost of placing an order of each product in each month follows
# the normal distribution with mean = 2, std = 1
np.random.seed(10)
o = np.random.normal(2,1,size = [T,N])

# assume holding cost of each product in each month follows 
# the normal distribution with mean = 1, std = 1
np.random.seed(10)
h = np.random.normal(1,1,size = [T,N])

# generate the samples of demand we have, assume discrete 
# uniform distribution between 30 and 50
np.random.seed(10)
d = np.random.randint(30,50,size = [10,T,N]) # 10 * T = 100

# Modelling
m = Model('Demand Uncertainty')

# variables
# amount of orders in each month of each prodcut
x = m.addVars(10,T,N,vtype = 'I',name = 'x')
# amount of inventory in each month of each product
y = m.addVars(10,T,N,vtype = 'I', name = 'y')


m.setObjective(1/10 * quicksum(p[i,j] * d[s,i,j] - o[i,j] * x[s,i,j] - h[i,j] * y[s,i,j]
	for s in range (10) for i in range(T) for j in range(N)),GRB.MAXIMIZE)

m.addConstrs((x[s,0,j] - y[s,0,j] == d[s,0,j] 
              for s in range(10) for j in range(N)),'first month')
m.addConstrs((x[s,i,j] + y[s,i-1,j] - y[s,i,j] == d[s,i,j]
              for s in range(10) for i in range(1,T) for j in range(N))
             , 'other months')


m.optimize()


print('Obj: %g' % m.objVal)

        




