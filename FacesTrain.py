import os
import cv2 as cv
import numpy as np
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
import sys
import ftplib
from ftplib import FTP


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

        face=cv.face.LBPHFaceRecognizer_create()
        face.train(features,labels)

        options = QtWidgets.QFileDialog.Options()
        #options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName1, _ = QtWidgets.QFileDialog.getSaveFileName(self, 
            "Save File", "", "YML files(*.yml)", options = options)
        

        

        options = QtWidgets.QFileDialog.Options()
        #options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName2, _ = QtWidgets.QFileDialog.getSaveFileName(self, 
            "Save File", "", "NPY files(*.npy)", options = options)
        

        options = QtWidgets.QFileDialog.Options()
        #options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName3, _ = QtWidgets.QFileDialog.getSaveFileName(self, 
            "Save File", "", "NPY files(*.npy)", options = options)
       

        face.save(fileName1)
        np.save(fileName2, features)
        np.save(fileName3, labels)

        ftp = FTP(host="192.168.0.101");
        ftp.login(user="Nitin V Kavya", passwd="nitinvkavya");
        folderName = self.ftp_dir
        if folderName not in ftp.nlst():
            ftp.mkd(folderName)
        ftp.quit()
        
        session = ftplib.FTP('192.168.0.101','Nitin V Kavya','nitinvkavya')
        session.cwd(folderName)

        file = open(fileName1,'rb')                  # file to send
        session.storbinary('STOR '+fileName1[fileName1.rindex('/')+1:len(fileName1)], file)     # send the file
        file.close()
        
        file = open(fileName2,'rb')                  # file to send
        session.storbinary('STOR '+fileName2[fileName2.rindex('/')+1:len(fileName2)], file)     # send the file
        file.close()   
        
        file = open(fileName3,'rb')                  # file to send
        session.storbinary('STOR '+fileName3[fileName3.rindex('/')+1:len(fileName3)], file)     # send the file
        file.close()   
                                           # close file and FTP
        session.quit()
        os.remove(fileName1)
        os.remove(fileName2)
        os.remove(fileName3)

    def create_train(self,dir,people,features,labels,haar_cascade):
        for person in people:
            path=os.path.join(str(dir),person)
            label=people.index(person)
            self.trainProgress.setValue(int((label+1)/(len(people))*100))
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


QPushButton:hover{
        background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 :   1, stop :   0.0 #ffd9aa,
                stop :   0.5 #ffbb6e, stop :   0.55 #feae42, stop :   1.0 #fedb74);
}

QPushButton {
        border: 1px solid #6593cf;
        border-radius: 2px;
        padding: 5px 15px 2px 5px;
        background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 :   1, stop :   0.0 #f5f9ff,
                stop :   0.5 #c7dfff, stop :   0.55 #afd2ff, stop :   1.0 #c0dbff);
        color: #006aff;
        font: bold large "Arial";
        height: 30px;
}

QPushButton:pressed {
        background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 :   1, stop :   0.0 #c0dbff,
        stop :   0.5 #cfd26f, stop :   0.55 #c7df6f, stop :   1.0 #f5f9ff);
        padding-top: 2px;
        padding-left: 3px;

}


QPushButton:on {
        background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 :   1, stop :   0.0 #5AA72D,
        stop :   0.5 #B3E296, stop :   0.55 #B3E296, stop :   1.0 #f5f9ff);
        padding-top: 2px;
        padding-left: 3px;
}

QProgressBar{

  	background-color: #ee303c;  
  border-radius: 4px; 
  transition: 0.4s linear;  
  transition-property: width, background-color;  
   background-color: #FCBC51; 
  width: 100%; 
  background-image: linear-gradient(
        45deg, rgb(252,163,17) 25%, 
        transparent 25%, transparent 50%, 
        rgb(252,163,17) 50%, rgb(252,163,17) 75%,
        transparent 75%, transparent); 
  animation: progressAnimationStrike 6s;
 
}



"""

app.setStyleSheet(style)
window = FacesTrain()
app.exec_()
