
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

addTriangle3DCenter(7,-46,44,70,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(50,46,44,70,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(22,0,-23,113,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(18,-62,-80,89,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(47,62,-80,89,chest_cover_cad_frame_id,positionDict)
addTriangle3DCenter(36,0,-120,105,chest_cover_cad_frame_id,positionDict)
