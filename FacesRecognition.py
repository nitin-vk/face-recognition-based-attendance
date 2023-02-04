import os,ftplib
import numpy as np
import cv2 as cv
from FaceDetectionModule import FaceDetectionModule
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QFileDialog,QMessageBox
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
        self.people=[]
        self.faces_read={}
        self.afterSelectFrame.hide()
        self.downloadBtn.hide()
        self.recognizeBtn.hide()
        self.frame_4.hide()
        self.frame_5.hide()
        self.frame_6.hide()
        self.frame_7.hide()
        self.frame_8.hide()
        self.ftpWidget.hide()
        self.sheetNameLabel.hide()
        self.sheetNameText.hide()
        self.spreadOkBtn.hide()
        self.spreadCancelBtn.hide()
        self.videoTypeWindow.hide()
        self.listWidget.hide()
        self.ftpButtonFrame.hide()
        self.localBtn.clicked.connect(self.serachLocalFiles)
        self.recognizeBtn.clicked.connect(self.recognizeFaces)
        self.cancelBtn.clicked.connect(self.hideVideoTypeWindow)
        self.okBtn.clicked.connect(self.startStreaming)
        self.spreadSheetBtn.hide()
        self.spreadSheetBtn.clicked.connect(self.invokeSpreadSheet)
        self.spreadOkBtn.clicked.connect(self.createSpreadSheet)
        self.spreadCancelBtn.clicked.connect(self.cancelSpread)
        self.ftpBtn.clicked.connect(self.ftpProcess)
        self.ftpCancelBtn.clicked.connect(self.cancelFtp)
        self.ftpConnectBtn.clicked.connect(self.connectFtp)

    def ftpProcess(self):
        self.ftpWidget.show()
        self.frame_8.show()
        self.ftpButtonFrame.show()

    def cancelFtp(self):
        self.ftpWidget.hide()
        self.frame_8.hide()
        self.ftpButtonFrame.hide()

    def connectFtp(self):
        #p = QProcess()
        #p.startDetached("C:\\Windows\\explorer.exe", ["ftp://NitinVKavya:NitinVKavya@192.168.0.103:21"])
        #self.yml_file=QFileDialog.getOpenFileName(self, 'Open file', 
        #'ftp://192.168.0.103',"YML files (*.yml)")
        FTP_IP=self.ftpIpTextBox.toPlainText()
        FTP_USERNAME=self.ftpUsernameTextBox.toPlainText()
        FTP_PASSWORD=self.ftpPasswordTextBox.toPlainText()
        #Connect to FTP server
        ftp = ftplib.FTP(FTP_IP, FTP_USERNAME, FTP_PASSWORD)
        #Get welcome message
        print(ftp.getwelcome())




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
        self.spreadSheetBtn.show()
        self.downloadBtn.setEnabled(False)
        self.spreadSheetBtn.setEnabled(False)
        self.recognizeBtn.show()

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
        spread=SpreadSheetModule(self.people)
        mytext = self.sheetNameText.toPlainText()
        if mytext=='':
            QMessageBox.about(self, "ERROR", "ENTER THE FILE NAME")
            return
        mytext=mytext+'.xlsx'
        isExist = os.path.exists(mytext)
        if isExist==False:
            spread.createSpreadSheet(mytext)
        spread.updateSpreadSheet(self.faces_read,mytext)


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
        dir=r"C:\Users\Nitin V Kavya\Desktop\College\Final_Year_project\Final_Year\Faces\train"
        l=30
        t=7
        haar_cascade = cv.CascadeClassifier(r'C:\Users\Nitin V Kavya\Desktop\python\OpenCV\haar_face.xml')
        
        for i in os.listdir(dir):
            self.people.append(i)
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

                cv.putText(img, str(self.people[label]), (20,20), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,255,0), thickness=2)
                self.faces_read.setdefault(self.people[label],[])
                self.faces_read[self.people[label]].append(confidence)
        
            cv.imshow('Detected Face', img)
            if cv.waitKey(20) & 0xFF==ord('b'):
                break

        capture.release()
        cv.destroyAllWindows()
        self.spreadSheetBtn.setEnabled(True)

app = QtWidgets.QApplication(sys.argv)
window = FacesRecognition()
app.exec_()


