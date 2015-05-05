# this script is used to compute transforms between the L_SOLE
#reference frame and the individual elements of the triangular
#taxels on the sole of the left foot.

#from numpy import matrix
import numpy as np
import iDynTree


N_TRIANGLES = 25 #number of triangular patches on foot sole
N_TAXELS = 10    #number of taxel elements per triangle

# numpy2idyn function gets a numpy matrix as an input argument
# and transforms into a Transform object of iDynTree class.
def numpy2idyn(transform):
	idynVector = np.reshape(transform,16)
	idynTransform = iDynTree.Transform(iDynTree.Rotation(idynVector[0],idynVector[1],idynVector[2], \
 idynVector[4],idynVector[5],idynVector[6], \
 idynVector[8],idynVector[9],idynVector[10]), \
                                           iDynTree.Position(idynVector[3],idynVector[7],idynVector[11]))
	return idynTransform



"""
computeTransform function reads the .dat files in the respective folders and numpy matrix data
to the numpy2idyn function.

.dat files consists of a 4x4 transformation matrix information of taxel/triangle frames with respect to the L_SOLE
extracted from the CAD files

File numbering starts from 0. 
Arguments :
left sole to triangle transformation : pathName = "L_SOLE_TRIANGLE"
				       fileName = "transform_L_SOLE_TRIANGLE"
				       N_FILES = N_TRIANGLES
				       
triangle to taxel transformation : pathName = "TAXEL_TRANS"
				       fileName = "transform_TAXELORIGIN_TAXEL"
				       N_FILES = N_TAXELS				     			
"""
def computeTransform(pathName,fileName,N_FILES):
	i = 0
	transform = []
	while( i < N_FILES ):
		np_data = np.genfromtxt(pathName + "/" + fileName + "(" + str(i) + ").dat", delimiter = ",")
		transform.append(numpy2idyn(np_data))
		i = i + 1
	return transform
	


print "Computing Transform between L_SOLE and TRIANGLE ORIGINS...."
transform_L_SOLE_TRIANGLE = []
transform_L_SOLE_TRIANGLE = computeTransform("L_SOLE_TRIANGLE","transform_L_SOLE_TRIANGLE",N_TRIANGLES)
p= 0
while( p < N_TRIANGLES ):
	#print transform_L_SOLE_TRIANGLE[p].getPosition().toString()
	p = p + 1


print "\n \n Computing Transform between Taxel origin (located on element 3) and other Taxel elements...."	
transform_TRIANGLE_TAXEL = []
transform_TRIANGLE_TAXEL = computeTransform("TAXEL_TRANS","transform_TAXELORIGIN_TAXEL",N_TAXELS)
p= 0
while( p < N_TAXELS):
	#print transform_TRIANGLE_TAXEL[p].getPosition().toString()
	p = p + 1



print "Compute position of each taxel element with respect to L_SOLE reference frame..."
k = 0
transform_L_SOLE_TAXEL = []
while( k < N_TRIANGLES ):
	l = 0
	while( l < N_TAXELS ):
		transform_L_SOLE_TAXEL.append(transform_L_SOLE_TRIANGLE[k]*transform_TRIANGLE_TAXEL[l])
		l = l + 1
	k = k + 1

out = open("left_foot_mesh.txt", 'w')
p = 0
while ( p < (N_TRIANGLES*N_TAXELS) ):
	out_str =  transform_L_SOLE_TAXEL[p].getPosition().toString()
	
	#print transform_L_SOLE_TAXEL[p].getPosition().toString()
	
	l = []
	for s in out_str.split():
		try:
		 	l.append(float(s))
		except ValueError:
			pass
	pos_x = l[0]/1000 #converting to m from mm
	pos_y = l[1]/1000 #converting to m from mm 
	pos_z = l[2]/1000 #converting to m from mm
	norm_x = 0
	norm_y = 0
	norm_z = 1 
	print "%f %f %f %f %f %f \n" %(pos_x,pos_y,pos_z,norm_x,norm_y,norm_z)
	out.write("%f %f %f %f %f %f \n" %(pos_x,pos_y,pos_z,norm_x,norm_y,norm_z))
	p = p + 1
out.close()	


	
	

