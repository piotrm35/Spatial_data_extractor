"""
author: Piotr Michałowski, Olsztyn, woj. W-M, Poland
piotrm35@hotmail.com
license: GPL v. 2
work begin: 26.07.2019
"""


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

DATA_FILE_PATH = 'C:\\Users\\michalowskip\\Documents\\tmp\\Spatial_data_extractor_0.1.0\\data_1.txt'
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
        output_geom = QgsGeometry.fromPointXY(QgsPointXY(float(xy_list[0].strip()), float(xy_list[1].strip())))
        output_feat.setGeometry(output_geom)
        (res, outFeats) = output_layer.dataProvider().addFeatures([output_feat])

print('SCRIPT STOP')

    
