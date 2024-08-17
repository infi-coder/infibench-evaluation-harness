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

img.save('tmp.bmp')

import cv2
a = cv2.imread('tmp0.png')
b = cv2.imread('tmp.bmp')
print('img difference:', np.linalg.norm(a-b))
assert np.linalg.norm(a-b) < 1e-4
