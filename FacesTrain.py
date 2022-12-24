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

        ftp = FTP(host="192.168.0.102");
        ftp.login(user="Nitin V Kavya", passwd="nitinvkavya");
        folderName = self.ftp_dir
        if folderName not in ftp.nlst():
            ftp.mkd(folderName)
        ftp.quit()
        
        session = ftplib.FTP('192.168.0.102','Nitin V Kavya','nitinvkavya')
        session.cwd(folderName)

        file = open(fileName1,'rb')                  # file to send
        session.storbinary('STOR faces_train.yml', file)     # send the file
        file.close()
        
        file = open(fileName2,'rb')                  # file to send
        session.storbinary('STOR features.npy', file)     # send the file
        file.close()   
        
        file = open(fileName3,'rb')                  # file to send
        session.storbinary('STOR labels.npy', file)     # send the file
        file.close()   
                                           # close file and FTP
        session.quit()


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
window = FacesTrain()
app.exec_()