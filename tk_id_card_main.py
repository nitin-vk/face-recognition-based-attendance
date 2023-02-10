from reportlab.pdfgen import canvas
import tkinter as tk
import os
 # update the path 
from reportlab.lib.units import inch
import cv2 as cv

 # import the template
#from tk_id_input import s_name,s_id,s_class,s_gender,s_filename #tkinter

## comment below values if you are using above Tkinter window
#s_filename='D:\\images\\rabbit_face2.jpg'
from tk_id_card_temp import my_temp
class TK_ID_CARD_MAIN:
    
    def __init__(self,usn,name,img_path):
        self.usn=usn
        self.name=name
        self.img_path=img_path
        my_path=os.path.join(r"D:\ID_CARDS",self.img_path+'.pdf')
        c = canvas.Canvas(my_path,pagesize=(600,300))
        c=my_temp(c) # run the template
        img_dir=os.path.join(r"C:\Users\Nitin V Kavya\Desktop\College\Final_Year_project\Final_Year\Faces\train",self.img_path)
        for i in os.listdir(img_dir):
            real_img=os.path.join(img_dir,i)
            img=cv.imread(real_img)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            faceCascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(30, 30)
                    )
            for (x, y, w, h) in faces:
                cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                roi_color = img[y:y + h, x:x + w] 
                print("[INFO] Object found. Saving locally.") 
                cv.imwrite('id_face.jpg', roi_color)       
            c.drawImage('id_face.jpg',2.2*inch,0.7*inch) #Add image
            break

###### Adding Collected data ####
        c.setFillColorRGB(0,0,1)
        c.setFont("Helvetica", 20)
        c.drawString(0.5*inch,1.7*inch,self.usn)
        c.drawString(0.5*inch,1.3*inch,self.name)    
        #c.drawString(0.5*inch,0.9*inch,"cse")    
        #c.drawString(0.5*inch,0.5*inch,"male")    
######
        c.showPage()
        c.save()

