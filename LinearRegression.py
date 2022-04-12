import matplotlib.pyplot as plt
import numpy as np
from DataAnalysis_Functions import linreg

# This script was used to demonstrate linear regression.
# It has now been incorporated in DataAnalysis_Functions.py
# See notes from Murty's ME Analysis from 10/10 for how this was developed
# It was checked with Excel

# Data
x = np.array([1, 2, 3, 4, 5])
y = np.array([9, 18, 35, 41, 49])

# S and V are matricies calculated by finding the best fit trendline through the data
# S = C*V
V = np.array([[len(x), sum(x)], [sum(x), sum(x*x)]])
S = np.array([[sum(y)], [sum(x*y)]])
print(V)
print(S)

# The coefficients of the trendline are found
# C = S*V^-1 
C = np.linalg.solve(V, S)
print(C.T)

# Double Check Coefficients
C2 = np.matmul(np.linalg.inv(V), S)
print(C2)

# Calculate the trendline values
TL = np.polyval(np.flip(C), x)
print(TL)

# Calculate the R-squared value
R2 = sum((TL - y)**2)
Rtot = sum((y - np.mean(y))**2)
R =  1 - R2/Rtot

print(R2, Rtot)
print(R)

# Check function in DataAnalysis_Functions.py
[TL2, R22] = linreg(x, y)

print('R22', R22)

#Plot
plt.scatter(x,y)
plt.plot(x, TL)
plt.plot(x, TL2, 'r--')
plt.show()