from gurobipy import *
import numpy as np
import pandas as pd

n2 = 60
# Generate the location points
# Set the seed when generating the clients' location
np.random.seed(n2)
C_location = -1 + 2 * np.random.random((n2,2)) 

# get the 25 clients' demand and location
n = 25
np.random.seed(25)
dem = np.random.uniform(0,25,size = n2)
HDC_ind = np.argpartition(dem, -n)[-n:] # index of the 25 highest demand clients
HDC_location = C_location[HDC_ind]

depot = np.array([1,1])

routing_location = np.append([depot],HDC_location,axis = 0)

# initialize the distance matrix
distance = np.zeros(shape = (n+1,n+1))

for i in range(n+1):
	for j in range(n+1):
	    distance[i,j] = np.sqrt(
          (routing_location[i][0] - routing_location[j][0])**2
          + (routing_location[i][1] - routing_location[j][1])**2)

# Modelling
m = Model('Single Vehicle Routing')

# variables
# variables encoding the tour
x = m.addVars(n+1,n+1,vtype = 'B',name = 'x')
# variables encoding the position in the tour
u = m.addVars(n+1,lb = 0,name = 'u')


m.setObjective(quicksum(x[i,j] * distance[i,j] 
	for i in range(n+1) for j in range(n+1)),GRB.MINIMIZE)

# degree constraints
m.addConstrs((quicksum(x[i,j] for i in range(n+1)) == 1 
	for j in range(n+1)),'indegree')
m.addConstrs((quicksum(x[j,i] for i in range(n+1)) == 1 
	for j in range(n+1)),'outdegree')
# position constraints
m.addConstr(u[0] == 1,'start')
m.addConstrs((u[i]-u[j]+1 <= (n+1)*(1-x[i,j]) for i in range(n+1) for j in range(1,n+1)),'position')


m.optimize()

results = pd.DataFrame(columns = ['Variables','Values'])
for j in m.getVars():
  results = results.append({'Variables':j.varName,'Values':j.x},ignore_index=True)
        #print('%s %g' % (j.varName, j.x))
results.to_excel("D:/Data File/Graduate-LSE/MA424 Modelling in Operations Research/Final Project/2.0 Vehicle Routing_result.xlsx")
        
print('Obj: %g' % m.objVal)
