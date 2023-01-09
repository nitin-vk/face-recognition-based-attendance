import cv2 as cv
import mediapipe as mp
import time
#nitin was here
class FaceDetectionModule:
    def __init__(self,min_detection_confidence=0.5, model_selection=0):
        self.min_detection_confidence = min_detection_confidence
        self.model_selection = model_selection

        self.faceD=mp.solutions.face_detection
        
        self.faceDetect=self.faceD.FaceDetection(0.75)
        self.mpdraw=mp.solutions.drawing_utils


    def findFace(self,img,draw=True):
        imgRGB=cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.result=self.faceDetect.process(imgRGB)
        bboxes=[]
    #print(result.detections)

        if self.result.detections:
            
            for id,detection in enumerate(self.result.detections):
        #mpdraw.draw_detection(img,detection)
        #print(id,detection)
                ih, iw, ic=img.shape
                bboxC=detection.location_data.relative_bounding_box
        #bboxD=detection.location_data.relative_keypoints
        #print(bboxC)
                bbox=int(bboxC.xmin * iw), int(bboxC.ymin * ih),int(bboxC.width * iw),int(bboxC.height * ih)
                bboxes.append([id,bbox])
                if draw:
                    img=self.fancyDraw(img,bbox)
        #bboxx=int(bboxD.x * iw),int(bboxD.y * ih)
        #print(bbox)
                    
        return img,bboxes

    def fancyDraw(self,img,bbox,l=30,t=7):
        x,y,w,h=bbox
        x1,y1=x+w,y+h
        cv.rectangle(img,bbox,(0,255,0),1)
        #top left
        cv.line(img,(x,y),(x+l,y),(0,255,0),t)
        cv.line(img,(x,y),(x,y+l),(0,255,0),t)
        
        #top right
        cv.line(img,(x1,y),(x1-l,y),(0,255,0),t)
        cv.line(img,(x1,y),(x1,y+l),(0,255,0),t)

        #bottom right
        cv.line(img,(x1,y1),(x1-l,y1),(0,255,0),t)
        cv.line(img,(x1,y1),(x1,y1-l),(0,255,0),t)

        #bottom left
        cv.line(img,(x,y1),(x+l,y1),(0,255,0),t)
        cv.line(img,(x,y1),(x,y1-l),(0,255,0),t)
        return img

           
    

def main():
    
    
    frame=cv.VideoCapture(r'C:\Users\Nitin V Kavya\Desktop\videoplayback.webm')
    pt=0
    f=FaceDetectionModule()
    while True:
        isTrue,img=frame.read()
        img,bboxes=f.findFace(img)
        ct=time.time()
        ftp=1/(ct-pt)
        pt=ct
        cv.putText(img,str(int(ftp)),(80,100),cv.FONT_HERSHEY_COMPLEX,3,(0,255,0),3)
        cv.imshow('img',img)
        if cv.waitKey(20) & 0xFF==ord('b'):
            break
    frame.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()