"""
/***************************************************************************
  Spatial_data_extractor.py

  QGIS plugin that adds a point from map website to given point layer.
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
SCRIPT_VERSION = '1.1.2'
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
        self.Add_pushButton.setEnabled(False)
        self.Input_raw_data_textEdit.textChanged.connect(self.Input_raw_data_textEdit_textChanged)
        self.About_pushButton.clicked.connect(self.about_pushButton_clicked)
        
        
    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        self.action.triggered.disconnect(self.run)
        self.Add_pushButton.clicked.disconnect(self.Add_pushButton_clicked)
        self.Input_raw_data_textEdit.textChanged.disconnect(self.Input_raw_data_textEdit_textChanged)
        self.About_pushButton.clicked.disconnect(self.about_pushButton_clicked)


    def run(self):
        self.set_output_layer()
        if self.output_layer is not None:
            self.show()
        

    #----------------------------------------------------------------------------------------------------------------
    # input widget methods
    

    def Add_pushButton_clicked(self):
        self.Add_pushButton.setEnabled(False)
        self.Input_raw_data_textEdit_is_clearing = True
        self.Input_raw_data_textEdit.clear()
        self.Input_raw_data_textEdit_is_clearing = False
        self.set_output_layer()
        if self.output_layer is None:
            self.Spatial_data_textEdit.clear()
            return
        tx = self.Spatial_data_textEdit.toPlainText()
        if tx and tx != self.previous_data:
            self.add_a_point_to_output_layer(tx)
            self.previous_data = tx
            self.Spatial_data_textEdit.setPlainText('The spatial data has been saved to output layer.')
        else:
            self.Spatial_data_textEdit.setPlainText('Add_pushButton_clicked - POINT NOT ADDED.')
        

    def Input_raw_data_textEdit_textChanged(self):
        if not self.Input_raw_data_textEdit_is_clearing:
            try:
                x = None
                y = None
                tx = self.Input_raw_data_textEdit.toPlainText()
                tx_list = tx.split(Setup.X_COORDINATE_PREFIX)[1].replace('\t', ' ').replace('\n', ' ').split(' ')
                for i in range(len(tx_list)):
                    x = tx_list[i].strip()
                    if len(x) > 0:
                        break
                x = float(x.replace(',', '.'))
                tx_list = tx.split(Setup.Y_COORDINATE_PREFIX)[1].replace('\t', ' ').replace('\n', ' ').split(' ')
                for i in range(len(tx_list)):
                    y = tx_list[i].strip()
                    if len(y) > 0:
                        break
                y = float(y.replace(',', '.'))
                if self.Swapped_coordinates_checkBox.isChecked():
                    tmp = x
                    x = y
                    y = tmp
                self.Spatial_data_textEdit.setPlainText(str(x) + ' ' + str(y))
                self.Add_pushButton.setEnabled(True)
            except:
                self.Spatial_data_textEdit.setPlainText('Input_raw_data_textEdit_textChanged ERROR')
                

    def about_pushButton_clicked(self):
        QtWidgets.QMessageBox.information(self, SCRIPT_TITLE, SCRIPT_TITLE + ' v. ' + SCRIPT_VERSION + '\n' + GENERAL_INFO)


    #----------------------------------------------------------------------------------------------------------------
    # work methods:


    def set_output_layer(self):
        try:
            self.output_layer = QgsProject.instance().mapLayersByName(Setup.OUTPUT_POINT_LAYER_NAME)[0]
        except:
            self.output_layer = None
            QtWidgets.QMessageBox.critical(self, SCRIPT_TITLE, "There is no '" + str(Setup.OUTPUT_POINT_LAYER_NAME) + "' layer.")
    

    def add_a_point_to_output_layer(self, coordinates):
        try:
            _output_feat = QgsFeature(self.output_layer.fields())
            _xy_list = coordinates.split(' ')
            _output_geom = QgsGeometry.fromPointXY(QgsPointXY(float(_xy_list[0].strip()), float(_xy_list[1].strip())))
            _output_feat.setGeometry(_output_geom)
            self.output_layer.dataProvider().addFeatures([_output_feat])
        except:
            self.Spatial_data_textEdit.setPlainText('add_a_point_to_output_layer ERROR')
    



