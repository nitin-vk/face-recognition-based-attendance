import os
import cv2 as cv
import numpy as np
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
import sys
import ftplib
from ftplib import FTP
from PyQt5.QtGui import QPixmap
import pyqt_design


class FacesTrain(QtWidgets.QMainWindow):
    def __init__(self):
        super(FacesTrain, self).__init__()
        uic.loadUi('FacesTrain.ui', self)
        self.show()
        self.dir=''
        self.haar_cascade=''
        self.ftp_dir=''
        self.selectXml.clicked.connect(self.selectXmlFile)
        self.selectDir.clicked.connect(self.selectDirectory)
        self.trainBtn.clicked.connect(self.trainFaces)
        self.progressFrame.hide()
        self.doneFrame.hide()

    def selectXmlFile(self):
        self.haar_cascade = QFileDialog.getOpenFileName(self, 'Open file', 
        'c:\\',"XML files (*.xml)")
        #print(str(self.haar_cascade))
        self.haar_cascade=str(self.haar_cascade)
        pos=self.haar_cascade.index(',')
        self.haar_cascade=self.haar_cascade[2:pos-1]
        #print(os.path.exists(str(self.haar_cascade)))
        

    def selectDirectory(self):
        self.dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.ftp_dir=str(self.dir[self.dir.rindex('/')+1:len(self.dir)])
        

    def trainFaces(self):
        if self.dir=='':
            print("Select the training directory")
            return

        if self.haar_cascade=='':
            print("select the XML file for haar cascading")
            return
        self.progressFrame.show()
        
        dir=self.dir
        people=[]
        print("from train {}".format(self.haar_cascade))
        haar_cascade=cv.CascadeClassifier(self.haar_cascade)
        for i in os.listdir(dir):
            people.append(i)
        print(people)
        features=[]
        labels=[]
        self.create_train(dir,people,features,labels,haar_cascade)
        #print("Training Done")
        self.doneFrame.show()
        features=np.array(features,dtype='object')
        labels=np.array(labels)
        face=cv.face.LBPHFaceRecognizer_create(radius=1,neighbors=3)
        face.train(features,labels)
        folderName=self.ftp_dir
        if os.path.exists('D:/Compiled Files/'+folderName)==False:
            os.mkdir('D:/Compiled Files/'+folderName)
        

        face.save('D:/Compiled Files/'+folderName+'/compiled.yml')
        np.save('D:/Compiled Files/'+folderName+'/features', features)
        np.save('D:/Compiled Files/'+folderName+'/labels', labels)

          

    def create_train(self,dir,people,features,labels,haar_cascade):
        for person in people:
            path=os.path.join(str(dir),person)
            label=people.index(person)
            self.trainProgress.setValue(int((label+1)/(len(people))*100))
            self.trainProgress.setTextVisible(False)
            #time.sleep(5)
            for img in os.listdir(path):
                img_path=os.path.join(path,img)
                img_array=cv.imread(img_path)
                if img_array is None:
                    continue
        

                gray=cv.cvtColor(img_array,cv.COLOR_BGR2GRAY)
                face_rect=haar_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=3)
                for (a,b,c,d) in face_rect:
                    face_boi=gray[b:b+d,a:a+c]
                    features.append(face_boi)
                    labels.append(label)
                    
    


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
