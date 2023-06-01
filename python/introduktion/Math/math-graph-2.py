# Import libraries
import matplotlib.pyplot as plt
import numpy as np
 
# Creating vectors X and Y
x = np.linspace(0, 10, 50)
y = x * 4 + 8

fig = plt.figure(figsize = (10, 5))
# Create the plot
plt.plot(x, y, marker = 'o')

plt.grid()
 
# Show the plot
plt.show()