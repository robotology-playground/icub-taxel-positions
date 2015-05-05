import numpy as np
#import iDynTree
import matplotlib.pyplot as plt
plt.axis([0,1,0,1])
np_data = np.genfromtxt("left_foot_mesh.txt", delimiter = " ")


point_x = []
point_y = []
point_z = []
l = 0

while ( l < 250 ):
	point_x.append((np_data[l][0]))
	point_y.append((np_data[l][1]))
	point_z.append((np_data[l][2]))
    	l = l + 1

n = range(0,250)

plt.plot(point_x,point_y,'ro')	

for i in n:
	plt.annotate(i,(point_x[i],point_y[i]))

plt.show()

    	
    	

