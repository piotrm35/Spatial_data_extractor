SCRIPT_TITLE = 'Spatial data extractor'
SCRIPT_VERSION = '0.1.0'
GENERAL_INFO = """
author: Piotr Michałowski, Olsztyn, woj. W-M, Poland
piotrm35@hotmail.com
license: GPL v. 2
work begin: 26.07.2019
"""

# Python 3.6.7

import os, sys
from PyQt5 import QtWidgets, uic
from Setup import Setup



class Spatial_data_extractor(QtWidgets.QWidget):

    def __init__(self):
        super(Spatial_data_extractor, self).__init__()
        self.base_path = os.sep.join(os.path.realpath(__file__).split(os.sep)[0:-1])
        uic.loadUi(os.path.join(self.base_path, 'ui', 'Spatial_data_extractor.ui'), self)
        self.setWindowTitle(SCRIPT_TITLE + ' v. ' + SCRIPT_VERSION)
        self.Add_pushButton.clicked.connect(self.Add_pushButton_clicked)
        self.Input_raw_data_textEdit.textChanged.connect(self.Input_raw_data_textEdit_textChanged)
        self.output_file = open(Setup.DATA_FILE_NAME, 'a')
        self.previous_data = '*****'
        
		
    def closeEvent(self, event):        # overriding the method
        self.output_file.close()
        self.Add_pushButton.clicked.disconnect(self.Add_pushButton_clicked)
        self.Input_raw_data_textEdit.textChanged.disconnect(self.Input_raw_data_textEdit_textChanged)
        event.accept()
        

    #----------------------------------------------------------------------------------------------------------------


    def Add_pushButton_clicked(self):
        self.Add_pushButton.setEnabled(False)
        tx = self.Spatial_data_textEdit.toPlainText()
        print('Add_pushButton_clicked - tx = ' + tx)
        if tx and tx != self.previous_data:
            self.output_file.write(tx + '\n')
            self.previous_data = tx
            self.Input_raw_data_textEdit.clear()
            self.Spatial_data_textEdit.setPlainText('The spatial data has been saved to output file.')
        else:
            print('Add_pushButton_clicked - tx NOT ADDED.')
        self.Add_pushButton.setEnabled(True)
        

    def Input_raw_data_textEdit_textChanged(self):
        if self.Add_pushButton.isEnabled():
            self.Add_pushButton.setEnabled(False)
            tx = self.Input_raw_data_textEdit.toPlainText()
            tx2 = tx.split('X:')[1].split(' ')
            x = tx2[1].strip()
            print('x = ' + x)
            y = tx2[3].split('WGS84')[0].strip()
            print('y = ' + y)
            self.Spatial_data_textEdit.setPlainText(x + ' ' + y)
            self.Add_pushButton.setEnabled(True)
    

#====================================================================================================================

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    spatial_data_extractor = Spatial_data_extractor()
    spatial_data_extractor.show()
    sys.exit(app.exec_())


