import os,ftplib
import numpy as np
import cv2 as cv
from FaceDetectionModule import FaceDetectionModule
from main import Main
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QProcess,QUrl
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from PyQt5.QtGui import QDesktopServices
import sys,pickle,face_recognition
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
        self.regisWidget.hide()
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
        'c:\\',"Text Files (*.txt)")
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
        unknown_face=False
        self.frame_4.hide()
        self.frame_5.hide()
        self.videoTypeWindow.hide()
        with open(self.yml_file, "rb") as fp:
            known_face_encodings, known_face_names = pickle.load(fp)
        self.usn=[]
        self.people=[]
        for i in known_face_names:
            self.usn.append(i.split('-')[0])
            self.people.append(i.split('-')[-1])
        if self.liveStreamBtn.isChecked():
            videoType=0
        elif self.capturedVideoBtn.isChecked():
            videoType=QFileDialog.getOpenFileName(self, 'Open file', 
            'c:\\',"VIDEO FILES (*.avi *.mp4)")
            videoType=str(videoType)
            pos=videoType.index(',')
            videoType=videoType[2:pos-1]
            print(os.path.exists(videoType))
        else:
              QMessageBox.about(self, "ERROR", "SELECT THE TYPE OF VIDEO")
              return
        face_locations = []
        face_encodings = []
        self.faces_read=[]
        video = cv.VideoCapture(videoType)
        while True:	
            check, frame = video.read()
            small_frame = cv.resize(frame, (0,0), fx=0.5, fy= 0.5)
            rgb_small_frame = small_frame[:,:,::-1]
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, np.array(face_encoding), tolerance = 0.6)
                face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)	
                try:
                    matches = face_recognition.compare_faces(known_face_encodings, np.array(face_encoding), tolerance = 0.6)
                    face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        face_names.append(name)
                        if name not in self.faces_read:
                            self.faces_read.append(name)
                except:
                    pass

            if len(face_names) == 0:
                for (top,right,bottom,left) in face_locations:
                    top*=2
                    right*=2
                    bottom*=2
                    left*=2
                    cv.rectangle(frame, (left,top),(right,bottom), (0,0,255), 2)
                    font = cv.FONT_HERSHEY_DUPLEX
                    cv.putText(frame, 'Unknown', (left, top), font, 0.8, (255,255,255),1)
                    unknown_face=True
            else:
                for (top,right,bottom,left), name in zip(face_locations, face_names):   
                    top*=2
                    right*=2
                    bottom*=2
                    left*=2
                    cv.rectangle(frame, (left,top),(right,bottom), (0,255,0), 2)
                    font = cv.FONT_HERSHEY_DUPLEX
                    cv.putText(frame, name, (left, top), font, 0.8, (255,255,255),1)

            cv.imshow("Face Recognition Panel",frame)

            if cv.waitKey(1) == ord('s'):
                break

        video.release()
        cv.destroyAllWindows()
        self.spreadSheetBtn.setEnabled(True)
        if unknown_face==True:
            self.regisWidget.show()
        #print(self.faces_read)




        

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


