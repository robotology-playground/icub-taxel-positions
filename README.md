# icub-taxel-positions
Scripts for extracting taxel (tactile elements) positions for the iCub humanoid robot skin. 

## Visualizing taxel 2D locations using iCubSkinGui configuration file
If you want to visualize the taxel locations, the script you are interested is 
[cad_extraction/torso/skinGui.py](cad_extraction/torso/skinGui.py).

The script depends on numpy, matplotlib and the [YARP Python bindings](http://www.yarp.it/yarp_swig.html#yarp_swig_python). 
It can be used as: 
~~~
python ./skinGui.py --from torso.ini
~~~
The script search for the file in the iCubSkinGui [context](http://www.yarp.it/yarp_data_dirs.html#datafiles_contextsrobots), so it should work fine if `iCubSkinGui` works fine in your computer.
