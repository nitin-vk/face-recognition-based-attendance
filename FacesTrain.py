import os
import cv2 as cv
import numpy as np
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog,QMessageBox
import sys
import ftplib
from ftplib import FTP
from PyQt5.QtGui import QPixmap
import pyqt_design,face_recognition,pickle


class FacesTrain(QtWidgets.QMainWindow):
    def __init__(self):
        super(FacesTrain, self).__init__()
        uic.loadUi('FacesTrain.ui', self)
        self.show()
        self.dir=''
        self.haar_cascade=''
        self.ftp_dir=''
        self.selectClassBtn.clicked.connect(self.selectDirectory)
        self.trainBtn.setEnabled(False)
        self.trainBtn.clicked.connect(self.trainFaces)
        self.progressFrame.hide()
        self.doneFrame.hide()

    
    def selectDirectory(self):
        #self.dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        #self.ftp_dir=str(self.dir[self.dir.rindex('/')+1:len(self.dir)])
        self.ftp_dir=os.path.join("D:/Faces",self.branchComboBox.currentText(),self.yearComboBox.currentText(),self.sectionComboBox.currentText())
        self.dir=self.ftp_dir
        if os.path.exists(self.dir)==False:
            QMessageBox.information(self, "ERROR", "Training Directory Does Not Exsist")
        else:
            self.trainBtn.setEnabled(True)

    def trainFaces(self):
        if self.dir=='':
            print("Select the training directory")
            return

       
        
        self.progressFrame.show()
        dir=self.dir
        known_face_encodings = []
        known_face_names=[]
        for i in os.listdir(dir):
            known_face_names.append(i)
        for i in os.listdir(dir):
            self.trainProgress.setValue(int((int(known_face_names.index(i))+1)/(len(known_face_names))*100))
            self.trainProgress.setTextVisible(False)
            for file in os.listdir(os.path.join(dir,i)):
                image = face_recognition.load_image_file(os.path.join(dir,i,file))
                face_encoding = face_recognition.face_encodings(image)[0]
                known_face_encodings.append(face_encoding)
        folderName=self.ftp_dir
        if os.path.exists(os.path.join("D:/Compiled Files",self.branchComboBox.currentText(),self.yearComboBox.currentText(),self.sectionComboBox.currentText()))==False:
            os.mkdir(os.path.join("D:/Compiled Files",self.branchComboBox.currentText(),self.yearComboBox.currentText(),self.sectionComboBox.currentText()))
        with open((os.path.join('D:/Compiled Files/',self.branchComboBox.currentText(),self.yearComboBox.currentText(),self.sectionComboBox.currentText(),'encodings.txt')), "wb") as fp:
            pickle.dump((known_face_encodings, known_face_names), fp)
        self.doneFrame.show()
        
                    
    


app = QtWidgets.QApplication(sys.argv)
style="""
FacesTrain{

}

QPushButton:open { /* when the button has its menu open */
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #dadbde, stop: 1 #f6f7fa);
}

QPushButton::menu-indicator {
    image: url(menu_indicator.png);
    subcontrol-origin: padding;
    subcontrol-position: bottom right;
}

QPushButton::menu-indicator:pressed, QPushButton::menu-indicator:open {
    position: relative;
    top: 2px; left: 2px; /* shift the arrow by 2 px */
}

QPushButton {
    border: 2px solid #8f8f91;
    border-radius:  8px;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #f6f7fa, stop: 1 #dadbde);
    min-width: 80px;
}

QPushButton:pressed {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #dadbde, stop: 1 #f6f7fa);
}

QPushButton:flat {
    border: none; /* no border for a flat push button */
}

QPushButton:default {
    border-color: navy; /* make the default button prominent */
}
QPushButton:hover{
        background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 :   1, stop :   0.0 #ffd9aa,
                stop :   0.5 #ffbb6e, stop :   0.55 #feae42, stop :   1.0 #fedb74);
}



QPushButton::menu-indicator {
    image: url(menu_indicator.png);
    subcontrol-origin: padding;
    subcontrol-position: bottom right;
}

QProgressBar {
    border: 2px solid #2196F3;
    border-radius: 5px;
    background-color: #E0E0E0;
}
QProgressBar::chunk {
    background-color: #CD96CD;
    width: 10px; 
    margin: 0.5px;
}

QWidget{
    background-color:#E0E0E0;
}

"""

app.setStyleSheet(style)
window = FacesTrain()
app.exec_()
