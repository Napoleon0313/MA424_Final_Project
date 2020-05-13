from gurobipy import *
import numpy as np
import pandas as pd

n1 = 15
n2 = 60
# Generate the location points
# Set the seed to 15 when generating the facilities' location
np.random.seed(n1)
F_location = -1 + 2 * np.random.random((n1,2))

# generate the clients' location
np.random.seed(n2)
C_location = -1 + 2 * np.random.random((n2,2)) 

# Coumpute the opening cost
f = np.zeros(shape = (n1,1))
for i in range(n1):
  f[i,0] = 100 * 3 ** -(abs(F_location[i][0]) + abs(F_location[i][1]))

# Compute the service cost
c = np.zeros(shape = (n1,n2))
for i in range(n1):
  for j in range(n2):
    c[i,j] = abs(F_location[i][0] - C_location[j][0]) 
    + abs(F_location[i][1] - C_location[j][1])
    
# Modelling
m = Model('warehousing')

# variables
y = m.addVars(n1,vtype = 'B',name = 'y') 
x = m.addVars(n1,n2,vtype = 'B',name = 'x')

m.setObjective((quicksum(y[i] * f[i] for i in range(n1)) 
	+ quicksum(c[i,j] * x[i,j] for i in range(n1) for j in range(n2))
	), GRB.MINIMIZE)

m.addConstrs((quicksum(x[i,j] for i in range(n1)) == 1
	for j in range(n2)),'service1')
m.addConstrs((x[i,j] <= y[i] for i in range(n1) for j in range(n2)),'service2')

m.optimize()


print('Obj: %g' % m.objVal)


