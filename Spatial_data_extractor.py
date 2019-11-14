"""
/***************************************************************************
  Spatial_data_extractor.py

  QGIS plugin that adds a point from iMap powered web site to given point layer.
  --------------------------------------
  Date : 14.11.2019
  Copyright: (C) 2019 by Piotr Michałowski
  Email: piotrm35@hotmail.com
/***************************************************************************
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as published
 * by the Free Software Foundation.
 *
 ***************************************************************************/
"""

SCRIPT_TITLE = 'Spatial data extractor'
SCRIPT_NAME = 'Spatial_data_extractor'
SCRIPT_VERSION = '1.0.0'
GENERAL_INFO = """
author: Piotr Michałowski, Olsztyn, woj. W-M, Poland
piotrm35@hotmail.com
license: GPL v. 2
work begin: 26.07.2019
"""

import os, sys
from PyQt5 import QtGui, QtWidgets, uic
from qgis.core import *
from qgis.utils import iface
from .Setup import Setup



class Spatial_data_extractor(QtWidgets.QMainWindow):

    def __init__(self, iface):
        super(Spatial_data_extractor, self).__init__()
        self.iface = iface
        self.base_path = os.sep.join(os.path.realpath(__file__).split(os.sep)[0:-1])
        self.icon = QtGui.QIcon(os.path.join(self.base_path, 'img', 'Spatial_data_extractor_ICON.png'))
        self.previous_data = '*****'
        self.Input_raw_data_textEdit_is_clearing = False
        self.output_layer = None


    #----------------------------------------------------------------------------------------------------------------
    # plugin methods:

    def initGui(self):
        self.action = QtWidgets.QAction(self.icon, SCRIPT_TITLE, self.iface.mainWindow())
        self.action.setObjectName(SCRIPT_NAME + '_action')
        self.iface.addToolBarIcon(self.action)
        self.action.triggered.connect(self.run)
        uic.loadUi(os.path.join(self.base_path, 'ui', 'Spatial_data_extractor.ui'), self)
        self.setWindowTitle(SCRIPT_TITLE + ' v. ' + SCRIPT_VERSION)
        self.Add_pushButton.clicked.connect(self.Add_pushButton_clicked)
        self.Input_raw_data_textEdit.textChanged.connect(self.Input_raw_data_textEdit_textChanged)
        self.Add_pushButton.setEnabled(False)
        self.About_pushButton.clicked.connect(self.about_pushButton_clicked)
        
        
        
    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        self.action.triggered.disconnect(self.run)
        self.Add_pushButton.clicked.disconnect(self.Add_pushButton_clicked)
        self.Input_raw_data_textEdit.textChanged.disconnect(self.Input_raw_data_textEdit_textChanged)
        self.About_pushButton.clicked.disconnect(self.about_pushButton_clicked)
        
        

    def run(self):
        try:
            self.output_layer = QgsProject.instance().mapLayersByName(Setup.OUTPUT_POINT_LAYER_NAME)[0]
            self.show()
        except:
            self.output_layer = None
            QtWidgets.QMessageBox.critical(self, SCRIPT_TITLE, "There is no '" + str(Setup.OUTPUT_POINT_LAYER_NAME) + "' layer.")
        

    #----------------------------------------------------------------------------------------------------------------
    # input widget methods
    

    def Add_pushButton_clicked(self):
        self.Add_pushButton.setEnabled(False)
        tx = self.Spatial_data_textEdit.toPlainText()
        if self.output_layer and tx and tx != self.previous_data:
            self.add_a_point_to_output_layer(tx)
            self.previous_data = tx
            self.Spatial_data_textEdit.setPlainText('The spatial data has been saved to output layer.')
        else:
            self.Spatial_data_textEdit.setPlainText('Add_pushButton_clicked - POINT NOT ADDED.')
        self.Input_raw_data_textEdit_is_clearing = True
        self.Input_raw_data_textEdit.clear()
        self.Input_raw_data_textEdit_is_clearing = False
        

    def Input_raw_data_textEdit_textChanged(self):
        if not self.Input_raw_data_textEdit_is_clearing:
            tx = self.Input_raw_data_textEdit.toPlainText()
            tx2 = tx.split('X:')[1].split(' ')
            x = tx2[1].strip()
            y = tx2[3].split('WGS84')[0].strip()
            self.Spatial_data_textEdit.setPlainText(x + ' ' + y)
            self.Add_pushButton.setEnabled(True)


    def about_pushButton_clicked(self):
        QtWidgets.QMessageBox.information(self, SCRIPT_TITLE, SCRIPT_TITLE + ' v. ' + SCRIPT_VERSION + '\n' + GENERAL_INFO)


    #----------------------------------------------------------------------------------------------------------------
    # work methods:

    def add_a_point_to_output_layer(self, coordinates):
        _output_feat = QgsFeature(self.output_layer.fields())
        _xy_list = coordinates.split(' ')
        _output_geom = QgsGeometry.fromPointXY(QgsPointXY(float(_xy_list[0].replace(',', '.').strip()), float(_xy_list[1].replace(',', '.').strip())))
        _output_feat.setGeometry(_output_geom)
        self.output_layer.dataProvider().addFeatures([_output_feat])
    
    



