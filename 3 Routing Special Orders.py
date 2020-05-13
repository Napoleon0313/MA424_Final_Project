from gurobipy import *
import numpy as np
import pandas as pd

n2 = 60
# Generate the location points
# Set the seed when generating the clients' location
np.random.seed(n2)
C_location = -1 + 2 * np.random.random((n2,2)) 

# Get the 25 clients' demand and location
n = 25
np.random.seed(25)
dem = np.random.uniform(0,25,size = n2)
HDC_ind = np.argpartition(dem, -n)[-n:] # index of the 25 highest demand clients
HDC_location = C_location[HDC_ind]

# Generate the location of the 2 new clients with priority
np.random.seed(2)
P_location = -1 + 2 * np.random.random((2,2))

depot = np.array([1,1])

# Combine the graph
routing_location = np.append(np.append([depot],P_location,axis = 0)
                             ,HDC_location,axis = 0)


# initialize the distance matrix(s)
distance = np.zeros(shape = (n+2+1,n+2+1))
for i in range(n+2+1):
  for j in range(n+2+1):
    distance[i,j] = np.sqrt(abs(routing_location[i][0] - routing_location[j][0])
                            + abs(routing_location[i][1] - routing_location[j][1]))


# set the distance between depot and the two new clients to be relatively small
for i in range(3):
  for j in range(1,3):
    distance[i,j] = distance[i,j] / 100


# Modelling
m = Model('Routing Special Orders')

# variables
# variables encoding the tour
x = m.addVars(n+2+1,n+2+1,vtype = 'B',name = 'x')
# variables encoding the position in the tour
u = m.addVars(n+2+1,lb = 0,name = 'u')


m.setObjective(quicksum(x[i,j] * distance[i,j] 
	for i in range(n+1) for j in range(n+1)),GRB.MINIMIZE)

# degree constraints
m.addConstrs((quicksum(x[i,j] for i in range(n+2+1)) == 1 
	for j in range(n+2+1)),'indegree')
m.addConstrs((quicksum(x[j,i] for i in range(n+2+1)) == 1 
	for j in range(n+2+1)),'outdegree')
# position constraints
m.addConstr(u[0] == 1,'start')
m.addConstrs((u[i]-u[j]+1 <= (n+2+1)*(1-x[i,j]) for i in range(n+2+1) for j in range(1,n+2+1)),'position')


m.optimize()

results = pd.DataFrame(columns = ['Variables','Values'])
for j in m.getVars():
  results = results.append({'Variables':j.varName,'Values':j.x},ignore_index=True)
        #print('%s %g' % (j.varName, j.x))
results.to_excel("D:/Data File/Graduate-LSE/MA424 Modelling in Operations Research/Final Project/3.0 Routing Special Orders_result.xlsx")
        
print('Obj: %g' % m.objVal)
#Actual_Obj = Obj + 99*(distance[0,1] + distance[1,2])
        



