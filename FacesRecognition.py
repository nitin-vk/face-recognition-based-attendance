import os,ftplib
import numpy as np
import cv2 as cv
from FaceDetectionModule import FaceDetectionModule
from main import Main
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QProcess,QUrl
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from PyQt5.QtGui import QDesktopServices
import sys
from SpreadSheetModule import SpreadSheetModule

class FacesRecognition(QtWidgets.QMainWindow):
    def __init__(self):
        super(FacesRecognition, self).__init__()
        uic.loadUi('FacesRecognition.ui', self)
        self.show()
        self.yml_file=''
        self.haar_cascade=''
        self.ftp_dir=''
        self.mytext=''
        self.spread=''
        self.usn=[]
        self.people=[]
        self.faces_read={}
        self.afterSelectFrame.hide()
        self.recognizeBtn.hide()
        self.frame_4.hide()
        self.frame_5.hide()
        self.frame_6.hide()
        self.frame_7.hide()
        self.sheetNameLabel.hide()
        self.sheetNameText.hide()
        self.spreadOkBtn.hide()
        self.spreadCancelBtn.hide()
        self.videoTypeWindow.hide()
        self.listWidget.hide()
        self.sendMailBtn.hide()
        self.localBtn.clicked.connect(self.serachLocalFiles)
        self.recognizeBtn.clicked.connect(self.recognizeFaces)
        self.cancelBtn.clicked.connect(self.hideVideoTypeWindow)
        self.okBtn.clicked.connect(self.startStreaming)
        self.spreadSheetBtn.hide()
        self.spreadSheetBtn.clicked.connect(self.invokeSpreadSheet)
        self.spreadOkBtn.clicked.connect(self.createSpreadSheet)
        self.spreadCancelBtn.clicked.connect(self.cancelSpread)
        self.ftpBtn.clicked.connect(self.ftpProcess)
        self.sendMailBtn.clicked.connect(self.sendMail)
        

    def sendMail(self):
        self.spread.sendMail(self.mytext)
        QMessageBox.about(self, "MAIL SENT", "MAIL SENT SUCCESSFULLY")

    def ftpProcess(self):
        mainobj=Main()
        
    def serachLocalFiles(self):
        self.yml_file=QFileDialog.getOpenFileName(self, 'Open file', 
        'c:\\',"YML files (*.yml)")
        print(self.yml_file)
        self.yml_file=str(self.yml_file)
        pos=self.yml_file.index(',')
        self.yml_file=self.yml_file[2:pos-1]
        pos=self.yml_file.rindex('/')
        yml_file=self.yml_file[pos+1:len(self.yml_file)+1]
        #print(self.yml_file)
        if self.yml_file!='':
            self.fileLocation.insertPlainText(yml_file)
        self.afterSelectFrame.show()
        self.spreadSheetBtn.show()
        self.spreadSheetBtn.setEnabled(False)
        self.recognizeBtn.show()
        self.sendMailBtn.show()
        self.sendMailBtn.setEnabled(False)
       


    def recognizeFaces(self):
        self.videoTypeWindow.show()
        self.frame_4.show()
        self.frame_5.show()

    def hideVideoTypeWindow(self):
        self.frame_4.hide()
        self.frame_5.hide()
        self.videoTypeWindow.hide()

    def invokeSpreadSheet(self):
        self.frame_6.show()
        self.frame_7.show()
        self.listWidget.show()
        self.sheetNameLabel.show()
        self.sheetNameText.show()
        self.spreadOkBtn.show()
        self.spreadCancelBtn.show()
       

    def cancelSpread(self):
        self.frame_6.hide()
        self.frame_7.hide()
        self.sheetNameLabel.hide()
        self.sheetNameText.hide()
        self.spreadOkBtn.hide()
        self.spreadCancelBtn.hide()
        self.listWidget.hide()
        

    def createSpreadSheet(self):
        self.frame_6.hide()
        self.frame_7.hide()
        self.sheetNameLabel.hide()
        self.sheetNameText.hide()
        self.spreadOkBtn.hide()
        self.spreadCancelBtn.hide()
        self.listWidget.hide()
        self.spread=SpreadSheetModule(self.people,self.usn)
        self.mytext = self.sheetNameText.toPlainText()
        if self.mytext=='':
            QMessageBox.about(self, "ERROR", "ENTER THE FILE NAME")
            return
        self.mytext=self.mytext+'.xlsx'
        isExist = os.path.exists(self.mytext)
        if isExist==False:
            self.spread.createSpreadSheet(self.mytext)
        self.spread.updateSpreadSheet(self.faces_read,self.mytext)
        self.sendMailBtn.setEnabled(True)


    def startStreaming(self):
        self.frame_4.hide()
        self.frame_5.hide()
        self.videoTypeWindow.hide()
        self.people=[]
        self.faces_read={}
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
        dir=r"D:\Faces\8CSEB"
        l=30
        t=7
        haar_cascade = cv.CascadeClassifier(r"C:\Users\Nitin V Kavya\Desktop\College\Final_Year_project\Final_Year\haar_face.xml")
        
        for i in os.listdir(dir):
            self.usn.append(i[0:10])
            self.people.append(i[11:len(i)])
        print(self.usn)
        print(self.people)


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
                print(f'Label = {self.people[label]} with a confidence of {confidence}')

                cv.putText(img, str(self.usn[label]+'-'+self.people[label]), (20,20), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,255,0), thickness=2)
                self.faces_read.setdefault(self.usn[label],[])
                if len(self.faces_read[self.usn[label]])<10:
                    self.faces_read[self.usn[label]].append(confidence)
                    self.faces_read[self.usn[label]].sort()
                else:
                    if confidence<self.faces_read[self.usn[label]][9]:
                        del self.faces_read[self.usn[label]][9]
                        self.faces_read[self.usn[label]].append(confidence)
                        self.faces_read[self.usn[label]].sort()

                    
        
            cv.imshow('Detected Face', img)
            if cv.waitKey(20) & 0xFF==ord('b'):
                break

        capture.release()
        cv.destroyAllWindows()
        self.spreadSheetBtn.setEnabled(True)
        print(self.faces_read)

app = QtWidgets.QApplication(sys.argv)
style="""
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














"""

app.setStyleSheet(style)
window = FacesRecognition()
app.exec_()


