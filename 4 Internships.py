from gurobipy import *
import numpy as np
import pandas as pd

I = 10
A = 30

# generate the applicants' and internship's preference
IP = np.zeros(shape = (I,A))
seed = I
for i in range(I):
  for j in range(A):
    np.random.seed(seed)
    IP[i,] = np.random.choice(A,A,replace = False)
    seed = seed + 1 # change the seed when generating preference for different internships

AP = np.zeros(shape = (A,I))
seed = A
for j in range(A):
  for i in range(I):
    np.random.seed(seed)
    AP[j,] = np.random.choice(I,I,replace = False)
    seed = seed + 1 # change the seed when generating preference for different applicants

# Modelling
m = Model('Stable Matchings')

# variables
# indicating whether (i,j) belongs to the matching output or not 
x = m.addVars(I,A,vtype = 'B',name = 'x')



m.setObjective(1
               ,GRB.MAXIMIZE)

# matching constraints
m.addConstrs((quicksum(x[i,j] for j in range(A)) == 1 
              for i in range(I)),'matching')
# stability constraints
m.addConstrs((x[i,j] + quicksum(x[i,q] for q in np.where(IP[i,] < IP[i,j])[0]) 
               + quicksum(x[p,j] for p in np.where(AP[j,] < AP[j,i])[0])>= 1 
              for i in range(I) for j in range(A)),'stability')


m.optimize()

results = pd.DataFrame(columns = ['Variables','Values'])
for j in m.getVars():
  results = results.append({'Variables':j.varName,'Values':j.x},ignore_index=True)
        #print('%s %g' % (j.varName, j.x))
#results.to_excel("D:/Data File/Graduate-LSE/MA424 Modelling in Operations Research/Final Project/4.0 Internships_result.xlsx")
        
print('Obj: %g' % m.objVal)
