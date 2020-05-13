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
HDC_dem = dem[HDC_ind]
HDC_location = C_location[HDC_ind]

depot = np.array([1,1])

# add the demand of depot to be 0
routing_dem = np.append(0,dem[HDC_ind])
routing_location = np.append([depot],HDC_location,axis = 0)

# initialize the distance matrix
distance = np.zeros(shape = (n+1,n+1))

for i in range(n+1):
	for j in range(n+1):
	    distance[i,j] = np.sqrt(
          (routing_location[i][0] - routing_location[j][0])**2
          + (routing_location[i][1] - routing_location[j][1])**2)

# input the assignment results from balanced load warehousing
datafile_path = 'D:/Data File/Graduate-LSE/MA424 Modelling in Operations Research/Final Project/2.2 input data from 1.2.xlsx'
y_pd = pd.read_excel(datafile_path,sheet_name = 0,header = 0,index_col = 0)
y = y_pd.as_matrix()

# Modelling
m = Model('Single Vehicle Routing')

# variables
K = 3 # 3 vehicles
# variables encoding the tour
x = m.addVars(n+1,n+1,K,vtype = 'B',name = 'x')
# variables encoding the position in the tour
u = m.addVars(n+1,K,lb = 0,name = 'u')


m.setObjective(quicksum(x[i,j,k] * distance[i,j] 
	for i in range(n+1) for j in range(n+1) for k in range(K)),GRB.MINIMIZE)


# 1.31(1)
m.addConstrs((quicksum(x[i,j,k] for j in range(n+1) if j != i) == quicksum(x[j,i,k] for j in range(n+1) if j != i)
	for i in range(n+1) for k in range(K)),'service21')
# 1.31(2)
m.addConstrs((quicksum(x[i,j,k] for j in range(n+1) if j != i) == y[i,k] 
    for i in range(n+1) for k in range(K)),'service22')
# position constraints
m.addConstrs((u[i,k]-u[j,k]+routing_dem[j] <= sum(HDC_dem)*(1-x[i,j,k]) for i in range(n+1) 
    for j in range(1,n+1) if i!=j for k in range(K)),'position1')
m.addConstrs((u[i,k] >= routing_dem[i] * y[i,k] for i in range(1,n+1) for k in range(K))
	,'position21')
m.addConstrs((u[i,k] <= sum(routing_dem) * y[i,k] for i in range(1,n+1) for k in range(K))
	,'position22')


m.optimize()

results = pd.DataFrame(columns = ['Variables','Values'])
for j in m.getVars():
  results = results.append({'Variables':j.varName,'Values':j.x},ignore_index=True)
        #print('%s %g' % (j.varName, j.x))
results.to_excel("D:/Data File/Graduate-LSE/MA424 Modelling in Operations Research/Final Project/2.2 Multiple Vehicles and Warehousing Routing_result.xlsx")
        
print('Obj: %g' % m.objVal)



