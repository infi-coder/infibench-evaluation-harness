import matplotlib
from matplotlib import pyplot as plt
import PIL
import numpy as np


x = np.array([0, 1, 2, 3, 4])
y = np.array([0., 1., 4., 9., 16.])

fig = plt.figure(figsize=(4, 3))
ax = plt.axes()
ax.plot(x, y)

fig.canvas.draw()
fig.savefig('tmp0.png')

img = transform(fig)
