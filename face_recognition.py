import os
import numpy as np
import cv2 as cv
from FaceDetectionModule import FaceDetectionModule
dir=r"D:\Faces\8CSEB"
l=30
t=7
haar_cascade = cv.CascadeClassifier(r'C:\Users\Nitin V Kavya\Desktop\python\OpenCV\haar_face.xml')

#people = ['Ben Afflek', 'Elton John', 'Jerry Seinfield', 'Madonna', 'Mindy Kaling', 'Nitin']
people = []
faces_read={}
for i in os.listdir(dir):
    people.append(i)
print(people)
# features = np.load('features.npy', allow_pickle=True)
# labels = np.load('labels.npy')

face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_trained.yml')

capture=cv.VideoCapture(0)
f=FaceDetectionModule()
while True:
    
    isTrue,img=capture.read()
#img = cv.imread(r"C:\Users\Nitin V Kavya\Desktop\python\OpenCV\Faces\val\elton_john\3.jpg")
    img,boxes=f.findFace(img)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #cv.imshow('Person', gray)

# Detect the face in the image
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
print(faces_read)
for i in faces_read.keys():
    faces_read[i].sort()

    if len(faces_read[i])>10:
        faces_read[i]=faces_read[i][0:10]
print(faces_read)
