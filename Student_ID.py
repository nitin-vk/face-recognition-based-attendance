from PyQt5 import QtWidgets, uic
import sys,os
from PyQt5.QtWidgets import QFileDialog,QMessageBox
import cv2 as cv
from FaceDetectionModule import FaceDetectionModule

class Student_ID(QtWidgets.QMainWindow):
    def __init__(self):
        super(Student_ID, self).__init__()
        uic.loadUi('Student_ID.ui', self)
        self.show()
        self.createIdButton.setEnabled(False)
        self.selectCompiledButton.clicked.connect(self.selectCompiledFile)
        self.createIdButton.clicked.connect(self.startRecognition)
        self.yml_file=''
        self.people=[]
        self.faces_read={}

    def selectCompiledFile(self):
        self.yml_file=QFileDialog.getOpenFileName(self, 'Open file', 
        'c:\\',"YML files (*.yml)")
        print(self.yml_file)
        self.yml_file=str(self.yml_file)
        pos=self.yml_file.index(',')
        self.yml_file=self.yml_file[2:pos-1]
        '''pos=self.yml_file.index(',')
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
        self.recognizeBtn.show()'''
        if self.yml_file!='':
            self.createIdButton.setEnabled(True)

    def startRecognition(self):
        self.people=[]
        self.faces_read={}
        videoType=0
        l=30
        t=7
        dir=r"C:\Users\Nitin V Kavya\Desktop\College\Final_Year_project\Final_Year\Faces\train"
        haar_cascade = cv.CascadeClassifier(r'C:\Users\Nitin V Kavya\Desktop\python\OpenCV\haar_face.xml')
        face_recognizer = cv.face.LBPHFaceRecognizer_create()
        face_recognizer.read(self.yml_file)
        for i in os.listdir(dir):
            self.people.append(i)
        print(self.people)

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
                if len(self.faces_read[self.people[label]])<10:
                    self.faces_read[self.people[label]].append(confidence)
                    self.faces_read[self.people[label]].sort()
                else:
                    if confidence<self.faces_read[self.people[label]][9]:
                        del self.faces_read[self.people[label]][9]
                        self.faces_read[self.people[label]].append(confidence)
                        self.faces_read[self.people[label]].sort()

                    
        
            cv.imshow('Detected Face', img)
            if cv.waitKey(20) & 0xFF==ord('b'):
                break

        capture.release()
        cv.destroyAllWindows()
        print(self.faces_read)





app = QtWidgets.QApplication(sys.argv)
window = Student_ID()
app.exec_()