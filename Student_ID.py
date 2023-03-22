from PyQt5 import QtWidgets, uic
import sys,os,face_recognition,pickle,numpy as np
from PyQt5.QtWidgets import QFileDialog,QMessageBox
import cv2 as cv
from PIL import Image
from html_id_card import HTML_ID_CARD

class Student_ID(QtWidgets.QMainWindow):
    def __init__(self):
        super(Student_ID, self).__init__()
        uic.loadUi('Student_ID.ui', self)
        self.show()
        self.submitBtn.clicked.connect(self.selectCompiledFile)
        self.createIdButton.clicked.connect(self.startRecognition)
        self.photoBtn.clicked.connect(self.takePhoto)
        self.yml_file=''
        self.capture=''
        self.idPhoto=''
        self.people=[]
        self.faces_read={}
        
    def takePhoto(self):
        self.capture = cv.VideoCapture(0)
        while True:
            ret, frame = self.capture.read()
            self.idPhoto = frame
            cv.imshow('take it',frame)
            if cv.waitKey(1) == ord('s'):
                break
        self.capture.release()
        cv.destroyAllWindows()
        img = Image.fromarray(self.idPhoto)
        img.save('face.jpg')
        

    def selectCompiledFile(self):
        self.yml_file=os.path.join('D:\Compiled Files',self.branchComboBox.currentText(),self.yearComboBox.currentText(),self.sectionComboBox.currentText(),"encodings.txt")
        if self.yml_file!='':
            self.createIdButton.setEnabled(True)

    def startRecognition(self):
        if self.yml_file=="":
            QMessageBox.warning(self,"error","Select a Compiled File")
            return
        if self.idPhoto=="":
            QMessageBox.warning(self,"error","Click your picture")
            return
        unknown_face=False
        with open(self.yml_file, "rb") as fp:
            known_face_encodings, known_face_names = pickle.load(fp)
        self.usn=[]
        self.people=[]
        for i in known_face_names:
            self.usn.append(i.split('-')[0])
            self.people.append(i.split('-')[-1])
        videoType=0
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
                    cv.putText(frame, 'Unknown', (left, top), font, 0.8, (0,0,0),1)
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
        self.photoBtn.setEnabled(True)
        recognized_usn=self.faces_read[0].split('-')[0]
        recognized_name=self.faces_read[0].split('-')[1]
        #self.idPhoto.save('face.jpg')
        id_card=HTML_ID_CARD(recognized_usn,recognized_name,self.branchComboBox.currentText(),self.yearComboBox.currentText(),self.sectionComboBox.currentText())
        id_card.HTMLgen()
        id_card.PDFgen(str(recognized_usn)+"-"+str(recognized_name))
        self.idPhoto=""
        self.yml_filr=""
        
        

    
app = QtWidgets.QApplication(sys.argv)
window = Student_ID()
app.exec_()