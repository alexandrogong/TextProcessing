# encode utf-8

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


# '''line pic'''
# x = np.linspace(-6*np.pi, 6*np.pi, 1000)
# y = np.sin(x)
# z = np.cos(x)+2
#
# y1 = [2]*1000
# z1 = np.cos(x) + 2
#
# fig = plt.figure()
# ax = Axes3D(fig)
# ax.plot(x, y, z)
# ax.plot(x, y)
# ax.plot(x, y1, z1)
# plt.show()

# '''bar pic'''
# fig = plt.figure()
# ax = Axes3D(fig)
#
# x = [0, 1, 2, 3, 4, 5, 6]
#
# for i in x:
#     y = [0, 1, 2, 3, 4, 5]
#     z = [1, 2, 3, 1, 2, 3]
#     ax.bar(y, z, i, zdir='y')
# plt.show()


'''curved surface gaussian distribution'''
fig = plt.figure()
ax = Axes3D(fig)

x = np.linspace(0, 100, 1000)
y = np.linspace(0, 100, 1000)

sigma = 10
u = 50

x, y = np.meshgrid(x, y)

z = (1/(np.sqrt(2*np.pi)*sigma))*np.exp((-1/(2*sigma**2))*((x-u)**2+(y-u)**2))
ax.plot_surface(x, y, z, cmap=plt.cm.winter)
plt.show()

