
# In this file we saved some data extracted the CAD models of the iCub
# In particular, we extracted the center of the circles of the covers 
# that are used to house the electronics of the triangles.. we use them 
# as an approximate reference of the 3D position of the center taxel in the world

# We extracted this data from the RC_TLR_017_P_007.prt part . 
# All the positions are expressed with respect to the 
# frame CS0 of Feature 907 of part RC_TLR_017_P_007.prt . 
# We refer to this frame hereafter as chest_cover_cad_frame 

# the transform between chest_cover_cad_frame and root_frame (with the
# joints of the torso all in 0.0 position

import iDynTree

# random id, just for iDynTree semantics check
chest_cover_cad_frame_id = 1
root_frame_id = 2

root_frame_T_chest_cover_cad_frame = \
    iDynTree.Transform(iDynTree.Rotation(   0,   0, -1.0, \
                                         -1.0,   0,    0, \
                                            0, 1.0,    0),\
                       iDynTree.Position(27.69,-0.07,76.3));
                       
root_frame_T_chest_cover_cad_frame.getSemantics().setPoint(chest_cover_cad_frame_id)    
root_frame_T_chest_cover_cad_frame.getSemantics().setOrientationFrame(chest_cover_cad_frame_id)
root_frame_T_chest_cover_cad_frame.getSemantics().setReferencePoint(root_frame_id)    
root_frame_T_chest_cover_cad_frame.getSemantics().setReferenceOrientationFrame(root_frame_id)   

# triangle center positions for some triangles in chest_cover_cad_frame,
# contained in a dictonary where the triangle number is the key

positionDict = {}

def addTriangle3DCenter(triangleNumber, x, y, z, ref_frame_id, positionDict):
    pos = iDynTree.Position(x,y,z);
    pos.getSemantics().setReferencePoint(ref_frame_id);
    pos.getSemantics().setCoordinateFrame(ref_frame_id);
    positionDict[triangleNumber] = root_frame_T_chest_cover_cad_frame*pos;


addTriangle3DCenter(5,-49,0,103,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(6,-49,34,86,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(7,-46,44,70,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(8,-16,36,90,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(9,-33,29,96,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(10,-33,12,105,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(11,-16,3,109,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(17,-62,-60,92,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(18,-62,-80,89,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(19,-48,-89,97,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(22,0,-23,113,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(23,17,-33,113,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(24,-17,-52,112,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(25,-17,-33,112,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(26,-33,-23,110,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(27,-49,-33,105,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(28,-49,-52,104,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(29,-33,-62,108,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(32,62,-60,93,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(33,49,-52,105,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(34,49,-33,106,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(35,-16,-110,104,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(36,0,-120,105,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(37,-16,-109,104,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(38,-17,-91,108,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(39,-33,-81,106,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(40,0,-61,112,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(41,0,-81,110,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(42,17,-91,108,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(43,33,-81,106,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(44,33,-62,109,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(45,17,-52,112,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(46,48,-89,97,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(47,62,-80,89,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(49,49,34,86,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(50,46,44,70,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(52,33,-23,111,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(56,0,30,98,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(57,0,-13,107,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(58,16,3,109,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(59,33,12,105,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(60,33,29,96,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(61,16,36,90,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(62,48,0,102,chest_cover_cad_frame_id,positionDict)
