Spatial data extractor

# Purpose
QGIS plugin that adds a point from map website to given point layer.

# How to start work
1) set a name of point layer in OUTPUT_POINT_LAYER_NAME variable in Setup.py file (if necessary)
2) set X_COORDINATE_PREFIX and Y_COORDINATE_PREFIX variables in Setup.py file (if necessary)
3) make new point layer (with coordinate system as in map website) named as in OUTPUT_POINT_LAYER_NAME in Setup.py file
4) open a map website (the website must give x and y coordinates with mentioned above prefixes as a text)
5) place mouse cursor on a desired position
6) press Ctrl+a and Ctrl+c
7) set focus to main text field of this plugin and press Ctrl+v
8) press [Add] button
9) set focus to QGIS and press F5 (refresh) to see added point (if necessary)
 
# License:
GNU General Public License, version 2
