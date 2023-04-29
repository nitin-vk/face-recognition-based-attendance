import os,socket
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
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 12345
        s.bind((host, port))
        s.listen(1)
        print('Server listening on {}:{}'.format(host, port))

        while True:
            conn, addr = s.accept()
            print('Received connection from {}'.format(addr))
            self.data = conn.recv(1024).decode()
            print('Received message: {}'.format(self.data))
            response = 'Training done'
            self.train()
            conn.send(response.encode())
            conn.close()

    def train(self):
        dir_list=self.data.split('-')
        dir=os.path.join("D:/Faces",dir_list[0],dir_list[1],dir_list[2])
        known_face_encodings=[]
        known_face_names=[]
        for i in os.listdir(dir):
            known_face_names.append(i)
        for i in os.listdir(dir):
            people_encodings=[]
            for file in os.listdir(os.path.join(dir,i)):
                image=face_recognition.load_image_file(os.path.join(dir,i,file))
                face_encoidng=face_recognition.face_encodings(image)[0]
                people_encodings.append(face_encoidng)
            people_avg=sum(people_encodings)/len(people_encodings)
            known_face_encodings.append(people_avg)
        if os.path.exists(os.path.join("D:/Compied Files",dir_list[0],dir_list[1],dir_list[2]))==False:
            os.makedirs(os.path.join("D:/Compied Files",dir_list[0],dir_list[1],dir_list[2]))
        with open((os.path.join("D:/Compied Files",dir_list[0],dir_list[1],dir_list[2],"encodings.txt")),"wb") as fp:
            pickle.dump((known_face_encodings,known_face_names),fp)
        print("Trained")
       

    
    def selectDirectory(self):
        #self.dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        #self.ftp_dir=str(self.dir[self.dir.rindex('/')+1:len(self.dir)])
        self.ftp_dir=os.path.join("D:/Faces",self.branchComboBox.currentText(),self.yearComboBox.currentText(),self.sectionComboBox.currentText())
        self.dir=self.ftp_dir
        if os.path.exists(self.dir)==False:
            QMessageBox.information(self, "ERROR", "Training Directory Does Not Exsist")
            self.ftp_dir=''
            self.dir=''
            return
        else:
            self.trainBtn.setEnabled(True)

    def trainFaces(self):
        if self.dir=='':
            print("Select the training directory")
            return

       
        self.doneFrame.hide()
        self.progressFrame.show()
        self.trainProgress.setStyleSheet("""
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
        """)
        dir=self.dir
        known_face_encodings = []
        known_face_names=[]
        for i in os.listdir(dir):
            known_face_names.append(i)
        for i in os.listdir(dir):
            people_encodings=[]
            self.trainProgress.setValue(int((int(known_face_names.index(i))+1)/(len(known_face_names))*100))
            self.trainProgress.setTextVisible(False)
            for file in os.listdir(os.path.join(dir,i)):
                image = face_recognition.load_image_file(os.path.join(dir,i,file))
                face_encoding = face_recognition.face_encodings(image)[0]
                people_encodings.append(face_encoding)
            people_avg=sum(people_encodings)/len(people_encodings)
            known_face_encodings.append(people_avg)
        folderName=self.ftp_dir
        if self.trainProgress.maximum():
            self.trainProgress.setStyleSheet("""
            QProgressBar {
            border: 2px solid #2196F3;
            border-radius: 5px;
            background-color: #E0E0E0;
                        }
        QProgressBar::chunk {
            background-color: green;
            width: 10px; 
            margin: 0.5px;
            }
        """)
        if os.path.exists(os.path.join("D:/Compiled Files",self.branchComboBox.currentText(),self.yearComboBox.currentText(),self.sectionComboBox.currentText()))==False:
            os.makedirs(os.path.join("D:/Compiled Files",self.branchComboBox.currentText(),self.yearComboBox.currentText(),self.sectionComboBox.currentText()))
        with open((os.path.join('D:/Compiled Files/',self.branchComboBox.currentText(),self.yearComboBox.currentText(),self.sectionComboBox.currentText(),'encodings.txt')), "wb") as fp:
            pickle.dump((known_face_encodings, known_face_names), fp)
        self.doneFrame.show()
        self.trainBtn.setEnabled(False)
        
                    
    


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
QComboBox {
    background-color: white;
    border: 1px solid gray;
    border-radius: 5px;
    padding: 2px;
    selection-background-color: lightgray;
}

QComboBox:drop-down {
    width: 25px;
    border-left: 1px solid gray;
}

QComboBox QAbstractItemView {
    background-color: white;
    border: 1px solid gray;
    selection-background-color: lightgray;
}


"""

app.setStyleSheet(style)
window = FacesTrain()
app.exec_()
