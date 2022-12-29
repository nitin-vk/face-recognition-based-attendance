import os
import numpy as np
import cv2 as cv
from FaceDetectionModule import FaceDetectionModule
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog,QMessageBox
import sys

class FacesRecognition(QtWidgets.QMainWindow):
    def __init__(self):
        super(FacesRecognition, self).__init__()
        uic.loadUi('FacesRecognition.ui', self)
        self.show()
        self.yml_file=''
        self.haar_cascade=''
        self.ftp_dir=''
        self.afterSelectFrame.hide()
        self.downloadBtn.hide()
        self.recognizeBtn.hide()
        self.frame_4.hide()
        self.frame_5.hide()
        self.videoTypeWindow.hide()
        self.localBtn.clicked.connect(self.serachLocalFiles)
        self.recognizeBtn.clicked.connect(self.recognizeFaces)
        self.cancelBtn.clicked.connect(self.hideVideoTypeWindow)
        self.okBtn.clicked.connect(self.startStreaming)


    def serachLocalFiles(self):
        self.yml_file=QFileDialog.getOpenFileName(self, 'Open file', 
        'c:\\',"YML files (*.yml)")
        self.yml_file=str(self.yml_file)
        pos=self.yml_file.index(',')
        self.yml_file=self.yml_file[2:pos-1]
        pos=self.yml_file.rindex('/')
        yml_file=self.yml_file[pos+1:len(self.yml_file)+1]
        #print(self.yml_file)
        if self.yml_file!='':
            self.fileLocation.insertPlainText(yml_file)
        self.afterSelectFrame.show()
        self.downloadBtn.show()
        self.downloadBtn.setEnabled(False)
        self.recognizeBtn.show()

    def recognizeFaces(self):
        self.videoTypeWindow.show()
        self.frame_4.show()
        self.frame_5.show()

    def hideVideoTypeWindow(self):
        self.frame_4.hide()
        self.frame_5.hide()
        self.videoTypeWindow.hide()

    def startStreaming(self):
        videoType=''
        if self.liveStreamBtn.isChecked():
            videoType=0
        elif self.capturedVideoBtn.isChecked():
            videoType=QFileDialog.getOpenFileName(self, 'Open file', 
            'c:\\',"VIDEO FILES (*.avi)")
            videoType=str(videoType)
            pos=videoType.index(',')
            videoType=videoType[2:pos-1]
        else:
              QMessageBox.about(self, "ERROR", "SELECT THE TYPE OF VIDEO")
              return
        print("videotype is {}".format(videoType))
        dir=r"C:\Users\Nitin V Kavya\Desktop\College\Final_Year_project\Final_Year\Faces\train"
        l=30
        t=7
        haar_cascade = cv.CascadeClassifier(r'C:\Users\Nitin V Kavya\Desktop\python\OpenCV\haar_face.xml')
        people = []
        faces_read={}
        for i in os.listdir(dir):
            people.append(i)
        print(people)


        face_recognizer = cv.face.LBPHFaceRecognizer_create()
        face_recognizer.read(self.yml_file)

        capture=cv.VideoCapture(videoType)
        f=FaceDetectionModule()
        while True:
    
            isTrue,img=capture.read()

            img,boxes=f.findFace(img)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    


            faces_rect = haar_cascade.detectMultiScale(gray, 1.1, 4)

            for (x,y,w,h) in faces_rect:
        
                x1,y1=x+w,y+h
                faces_roi = gray[y:y+h,x:x+w]

                label, confidence = face_recognizer.predict(faces_roi)
                print(f'Label = {people[label]} with a confidence of {confidence}')

                cv.putText(img, str(people[label]), (20,20), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,255,0), thickness=2)
                faces_read.setdefault(people[label],[])
                faces_read[people[label]].append(confidence)
        
            cv.imshow('Detected Face', img)
            if cv.waitKey(20) & 0xFF==ord('b'):
                break

        capture.release()
        cv.destroyAllWindows()

app = QtWidgets.QApplication(sys.argv)
window = FacesRecognition()
app.exec_()


