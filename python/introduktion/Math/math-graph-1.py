# Import libraries
import matplotlib.pyplot as plt
import numpy as np

x = [1, 2, 5, 10]
y = [2, 4, 7, 9]

plt.plot(x, y, marker='o', linewidth=2)
plt.axis([0, 15, 0, 15])

for i, j in zip(x, y):
   plt.text(i, j+0.5, '({}, {})'.format(i, j))

plt.show()