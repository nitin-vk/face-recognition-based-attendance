import os
import cv2 as cv
import numpy as np
import face_recognition
import pickle

def create_train():
    dir=r"D:\Faces\CSE\4\B"
    known_face_encodings = []
    known_face_names=[]
    for i in os.listdir(dir):
        known_face_names.append(i)
        for file in os.listdir(os.path.join(dir,i)):
            print(os.path.join(dir,i,file))
            image = face_recognition.load_image_file(os.path.join(dir,i,file))
            #print(image)
            face_encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(face_encoding)
    with open("encodings.txt", "wb") as fp:
        pickle.dump((known_face_encodings, known_face_names), fp)

create_train()