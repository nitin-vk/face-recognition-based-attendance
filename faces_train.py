import os
import cv2 as cv
import numpy as np
dir=r"D:\Faces\8CSEB"
people=[]
haar_cascade=cv.CascadeClassifier(r"C:\Users\Nitin V Kavya\Desktop\python\OpenCV\haar_face.xml")
for i in os.listdir(dir):
    people.append(i)
print(people)
features=[]
labels=[]

def create_train():
    for person in people:
        path=os.path.join(dir,person)
        label=people.index(person)

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

create_train()
print("Training Done")

features=np.array(features,dtype='object')
labels=np.array(labels)

face=cv.face.LBPHFaceRecognizer_create(radius=1,neighbors=4)
face.train(features,labels)

face.save('face_trained.yml')
np.save('features.npy', features)
np.save('labels.npy', labels)