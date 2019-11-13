"""
author: Piotr Michałowski, Olsztyn, woj. W-M, Poland
piotrm35@hotmail.com
license: GPL v. 2
work begin: 26.07.2019
"""

# Usage:
# 1) set DATA_FILE_PATH
# 2) make new temporary point layer named as in OUTPUT_POINT_LAYER_NAME
# 3) open QGIS Python console
# 4) load this script and run it


from qgis.core import (
    QgsGeometry,
    QgsPoint,
    QgsPointXY,
    QgsWkbTypes,
    QgsProject,
    QgsFeatureRequest,
    QgsDistanceArea,
    QgsMapLayer
)

DATA_FILE_PATH = 'J:\\Dokumenty_2\\tmp\\QGIS_3\\Spatial_data_extractor_0.1.1\\data_3.txt'
OUTPUT_POINT_LAYER_NAME = 'Nowa warstwa tymczasowa'


print('SCRIPT START')

output_layer = QgsProject.instance().mapLayersByName(OUTPUT_POINT_LAYER_NAME)[0]
input_file = open(DATA_FILE_PATH, 'r')
data = input_file.read()
input_file.close()
lines = data.split('\n')
for line in lines:
    if line:
        print('line = ' + line)
        output_feat = QgsFeature(output_layer.fields())
        xy_list = line.split(' ')
        output_geom = QgsGeometry.fromPointXY(QgsPointXY(float(xy_list[0].replace(',', '.').strip()), float(xy_list[1].replace(',', '.').strip())))
        output_feat.setGeometry(output_geom)
        (res, outFeats) = output_layer.dataProvider().addFeatures([output_feat])

print('SCRIPT STOP')

    
