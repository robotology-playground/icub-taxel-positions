#!/usr/bin/env python 

import yarp
import numpy as np
import matplotlib.pyplot as plt
import sys
from mpl_toolkits.mplot3d import Axes3D
import scipy.interpolate



# workaround because ResourceFinder::configure is not properly typemapped 
# in python

# Load yarp ResourceFinder 
rf = yarp.ResourceFinder()
rf.setVerbose();
# Set the same default context of the iCubSkinGui for convenience
rf.setDefaultContext("skinGui/skinGui");

if( "--from" not in sys.argv ):
    print("Usage : skinGui.py --from nameOfSkinGuiConfiguration.ini")
    skinGuiFileName = "torso.ini"
else:
    skinGuiFileName = sys.argv[sys.argv.index("--from")+1]

prop = yarp.Property();
prop.fromConfigFile(rf.findFileByName(skinGuiFileName));

print("Reading taxel positions from " + rf.findFileByName(skinGuiFileName))

sens_group = prop.findGroup("SENSORS")

triangleSide = 30
triangleVertices = []
triangleVertices.append(np.array([0.0, np.sqrt(3)*triangleSide/3]))
triangleVertices.append(np.array([triangleSide/2, -np.sqrt(3)*triangleSide/6]))
triangleVertices.append(np.array([-triangleSide/2, -np.sqrt(3)*triangleSide/6]))

triangles = []
trianglesDict = {}
for i in range(1,sens_group.size()):
    triangle_group = sens_group.get(i).asList();
    triangle = {}
    triangle["type"]   = triangle_group.get(0).asString();
    triangle["number"] = triangle_group.get(1).asInt();
    triangle["u"]      = triangle_group.get(2).asInt();
    triangle["v"]      = triangle_group.get(3).asInt();
    triangle["orient"] = triangle_group.get(4).asInt();
    triangle["gain"]   = triangle_group.get(5).asInt();
    triangle["mirror"] = triangle_group.get(6).asInt();
    
    # saving triangle vertices in u/v space
    theta = np.pi*triangle["orient"]/180.0
    rotMatrix = np.array([[np.cos(theta), -np.sin(theta)], 
                          [np.sin(theta),  np.cos(theta)]])
    off = np.array([triangle["u"],triangle["v"]])
    triangle["vertex1"] = rotMatrix.dot(triangleVertices[0]) + off;
    triangle["vertex2"] = rotMatrix.dot(triangleVertices[1]) + off;
    triangle["vertex3"] = rotMatrix.dot(triangleVertices[2]) + off;
                                

    triangles.append(triangle)
    trianglesDict[triangle["number"]] = triangle
    
# sort the triangle list based on number (id)
triangles.sort(lambda x,y : cmp(x['number'], y['number']))

# taxel positions in triangle frame (expressed in millimeters
taxelsPosInTriangle = []
# taxel 0
taxelsPosInTriangle.append(np.array([6.533, 0.0]))
# taxel 1
taxelsPosInTriangle.append(np.array([9.8, -5.66]))
# taxel 2
taxelsPosInTriangle.append(np.array([3.267, -5.66]))
# taxel 3 
taxelsPosInTriangle.append(np.array([0.0, 0.0]))
# taxel 4
taxelsPosInTriangle.append(np.array([-3.267, -5.66]))
# taxel 5
taxelsPosInTriangle.append(np.array([-9.8, -5.66]))
# taxel 6 (thermal pad!)
taxelsPosInTriangle.append(np.array([-6.533, -3.75]))
# taxel 7  
taxelsPosInTriangle.append(np.array([-6.533, 0]))
# taxel 8
taxelsPosInTriangle.append(np.array([-3.267, 5.66]))
# taxel 9 
taxelsPosInTriangle.append(np.array([0.0, 11.317]))
# taxel 10 (thermal pad)
taxelsPosInTriangle.append(np.array([0, 7.507]))
# taxel 11 
taxelsPosInTriangle.append(np.array([3.267, 5.66]))

# generate taxel list, we allocate a list of the total number of triangles
# dummy values (for the torso are 64) and then we overwrite the taxels 
# for the real triangles 
dummy_taxel = {}
dummy_taxel["type"] = "dummy"
# we put arbitrary big values of u and v so we don't have to worry about this
# dummy taxel interpolation
dummy_taxel["u"] = 10000;
dummy_taxel["v"] = 10000;


# the total number of the triangles is composed by both real triangles
# and dummy triangles, is given by the length of the yarp vector published
# on the port, divided by 12 (for the torso: 768/12 = 64)
total_number_of_triangles = 64

# number of taxels for triangle
taxel_per_triangle = 12

# list of taxels (from 0 to taxel_per_triangle) that are thermal 
thermal_taxels_list = [6,10]

# taxel that is the center of the triangle
center_taxel = 3;

taxels = total_number_of_triangles*taxel_per_triangle*[dummy_taxel]

for triangle in triangles:
    for i in range(0,taxel_per_triangle):
        theta = np.pi*triangle["orient"]/180
        rotMatrix = np.array([[np.cos(theta), -np.sin(theta)], 
                                [np.sin(theta),  np.cos(theta)]])
        offset = rotMatrix.dot(taxelsPosInTriangle[i])
        
        taxel = {}
        
        # index of the taxel in the skin part YARP port
        taxel["index"] = triangle["number"]*taxel_per_triangle+i;
        taxel["triangleNumber"] = triangle["number"]

        if( i in thermal_taxels_list ):
            taxel["type"] = "thermal"
            # u,v are the coordinates in millimeters of the taxels in 
            # the iCubSkinGui 
            # compute the offset of the taxel with respect to the triangle center                                
            taxel["u"] = triangle["u"] + offset[0]
            taxel["v"] = triangle["v"] + offset[1]
            
            # the taxel x, y, z position in root frame will be filled by
            # the interpolation procedure
        else:
            taxel["type"] = "tactile"
            taxel["u"] = triangle["u"] + offset[0]
            taxel["v"] = triangle["v"] + offset[1]
            taxel["x"] = None
            taxel["y"] = None
            taxel["z"] = None

        taxels[taxel["index"]] = taxel
        

variables= {}
execfile( "torsoTrianglesCAD.py", variables )

root_frame_T_chest_cover_cad_frame = variables["root_frame_T_chest_cover_cad_frame"]
positionDict = variables["positionDict"]

# plot 3d data 
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
point_x3d = []
point_y3d = []
point_z3d = []
for key in positionDict:
    point_x3d.append(positionDict[key](0));
    point_y3d.append(positionDict[key](1));
    point_z3d.append(positionDict[key](2));
    
ax.plot(point_x3d,point_y3d,point_z3d,'o');
ax.axis('equal')

for key in positionDict:
    label = "ID: " + str(trianglesDict[key]["number"]);
    ax.text(positionDict[key](0),positionDict[key](1),positionDict[key](2),label)
    
# interpolate ! 
trainingPoints = ([],[])
unknownPoints = ([],[])
valuesX = []
valuesY = []
valuesZ = []
for key in positionDict:
    trainingPoints[0].append(trianglesDict[key]["u"]);
    trainingPoints[1].append(trianglesDict[key]["v"]);
    valuesX.append(positionDict[key](0))
    valuesY.append(positionDict[key](1));
    valuesZ.append(positionDict[key](2));

for taxel in taxels:
    unknownPoints[0].append(taxel["u"]);
    unknownPoints[1].append(taxel["v"]);
        

unknownX = scipy.interpolate.griddata(np.array(trainingPoints).T, np.array(valuesX), np.array(unknownPoints).T, method="cubic")
unknownY = scipy.interpolate.griddata(np.array(trainingPoints).T, np.array(valuesY), np.array(unknownPoints).T, method="cubic")
unknownZ = scipy.interpolate.griddata(np.array(trainingPoints).T, np.array(valuesZ), np.array(unknownPoints).T, method="cubic")

# the taxel outside the 2D convex hull of the triangle center, use the triangle center
for taxelIndex in range(0,len(unknownX)):
    taxel = taxels[taxelIndex]
    if( np.isnan(unknownX[taxelIndex]) and not(taxel["type"] is "dummy") ):
        unknownX[taxelIndex] = positionDict[taxel["triangleNumber"]](0)
        unknownY[taxelIndex] = positionDict[taxel["triangleNumber"]](1)
        unknownZ[taxelIndex] = positionDict[taxel["triangleNumber"]](2)

ax.plot(unknownX,unknownY,unknownZ,'.',c="blue");
#for key in unknownPointsKeys:
#    label = "ID: " + str(trianglesDict[key]["number"]);
#    ax.text(unknownX[unknownPointsKeys.index(key)],unknownY[unknownPointsKeys.index(key)],unknownZ[unknownPointsKeys.index(key)],label)
ax.plot(point_x3d,point_y3d,point_z3d,'o',c="red");

# export the 3d points to a skinManager "positions" compatible file
def exportSkinManagerPositionTxtFile(taxels,posx,posy,posz,normx,normy,normz,name,filename):
    assert(len(taxels) == len(posx))
    assert(len(taxels) == len(posy))
    assert(len(taxels) == len(posz))
    assert(len(taxels) == len(normx))
    assert(len(taxels) == len(normy))
    assert(len(taxels) == len(normz))
    out_file = open(filename,"w");
    out_file.write("name    " + name + "\n");
    out_file.write("spatial_sampling     taxel\n");
    # the convention relative to taxel2repr is that dummy taxels are 
    # mapped to -1, temperature taxel are mapped -2 and tacticle taxels
    # are mapped to the index of the taxel that is the center of the triangle
    out_file.write("taxel2Repr ( ")
    for taxel in taxels:
        if( taxel["type"] == "dummy" ):
            out_file.write(" -1 ");
        elif( taxel["type"] == "thermal"):
            out_file.write(" -2 ");
        elif( taxel["type"] == "tactile"):
            out_file.write(" " + str(taxel["triangleNumber"]*taxel_per_triangle+center_taxel) + " ");
        else:
            assert(false)
            
    out_file.write(" )\n");
    
    # out write 
    out_file.write("[calibration]\n");
    for taxel in taxels:
        if( taxel["type"] == "dummy" ):
            out_file.write("0.0 0.0 0.0 0.0 0.0 0.0 \n");
        elif( taxel["type"] == "thermal" or taxel["type"] == "tactile"):
            taxelIndex = taxel["index"]
            out_file.write(str(posx[taxelIndex]/1000) + " " +  str(posy[taxelIndex]/1000) + " " +  str(posz[taxelIndex]/1000) + \
                           " " + str(normx[taxelIndex]) + " " +  str(normy[taxelIndex]) + " " + str(normz[taxelIndex]) + "\n");
        else:
            assert(false)
    out_file.write("\n")

#normal for now are set to the x direction
normx = [1.0]*len(unknownX)
normy = [0.0]*len(unknownX)
normz = [0.0]*len(unknownX)

exportSkinManagerPositionTxtFile(taxels,unknownX,unknownY,unknownZ,normx,normy,normz,"chest","torso.txt");


# 2d plot
fig2 = plt.figure()
rect = 0,1,0,1
triangleAx = fig2.add_subplot(1, 2, 1)
taxelAx = fig2.add_subplot(1, 2, 2)



point_x = []
point_y = []
point_z = []

for triangle in triangles:
    point_x.append(triangle["u"])
    point_y.append(triangle["v"])
    point_z.append(0.0)

triangleAx.set_xlim(np.min(point_x)-5,np.max(point_x)+5)
triangleAx.set_ylim(np.min(point_y)-5,np.max(point_y)+5)
taxelAx.set_xlim(np.min(point_x)-20,np.max(point_x)+20)
taxelAx.set_ylim(np.min(point_y)-20,np.max(point_y)+20)

#triangleAx.plot(point_x,point_y,'ro') 
# draw triangle
for triangle in triangles:
    xy = np.vstack([triangle["vertex1"],triangle["vertex2"],triangle["vertex3"]])
    label = "ID: " + str(triangle["number"]);
    triangleAx.add_patch(plt.Polygon(xy, color=[0.22745, 0.4, 0.16], label=label, closed=True))
    taxelAx.add_patch(plt.Polygon(xy, color=[0.22745, 0.4, 0.16], label=label, closed=True))

for i in range(0,len(triangles)):
    label = "N: " + str(triangles[i]["number"]) + "\n" + "I: " + str(i);
    triangleAx.annotate(label,(point_x[i],point_y[i]),ha='center',va='center')
    
for taxel in taxels:
    if( taxel["type"] == "tactile" ):
        xy = (taxel["u"],taxel["v"])
        taxelAx.add_patch(plt.Circle(xy, 2, color=[0.99, 0.99, 0.05]))
        label = str(taxel["index"])
        taxelAx.annotate(label,xy,ha='center',va='center')

    
    
triangleAx.axis('equal')
plt.show()




