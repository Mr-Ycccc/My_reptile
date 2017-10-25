import numpy as np
import matplotlib.pyplot as plt
import random
import pandas

'''
point=np.arange(0.5,5,0.01)
xs,ys=np.meshgrid(point,point)
z=np.sqrt(xs**2+ys**2)
plt.imshow(z,cmap=plt.cm.gray)
plt.colorbar()
plt.title("Image plot of $\sqrt{x^2+y^2}$ for a grid of values")
'''


position=0
walk=[position]
steps=1000
for i in range(steps):
	step=1 if random.randint(0,1) else -1
	position+=step
	walk.append(position)