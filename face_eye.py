import cv2
import numpy as np
import imutils

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('C:\\Anaconda3\\pkgs\\opencv-3.3.0-py36_202\\Library\\etc\\haarcascades\\haarcascade_frontalface_default.xml')
if face_cascade.empty() :
	print("Error with the file")
    # file couldn't load, give up!

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('C:\\Anaconda3\\pkgs\\opencv-3.3.0-py36_202\\Library\\etc\\haarcascades\\haarcascade_eye.xml')
body_cascade = cv2.CascadeClassifier('C:\\Anaconda3\\pkgs\\opencv-3.3.0-py36_202\\Library\\etc\\haarcascades\\haarcascade_lowerbody.xml')
cap = cv2.VideoCapture(0)
#cap = cv2.imread('man.jpg')

while True:
	#img=cv2.VideoCapture(0)
	ret,img =cap.read()
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3 , 5)
	bodies = body_cascade.detectMultiScale(gray,1.1,4 )
	for (x,y,w,h) in faces:
		cv2.rectangle(img, (x, y),(x+w, y+h), (255,0,0), 2 )
		#(x,y) is starting point
		#(x+w,y+h) is the ending point
		#(255,0,0) - > blue rectangle
		# 2 is the alignment

		#eye inside face
		#region of interest
		roi_gray = gray[y:y+h,x:x+w]
		roi_color = img[y:y+h, x:x+w]
		eyes =eye_cascade.detectMultiScale(roi_gray)
		for(ex,ey,ew,eh) in eyes:
			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
	#img=imutils.resize(img, width=min(100, img.shape[1]))
	for (bx,by,bw,bh) in bodies:
		cv2.rectangle(img, (bx,by), (bx+bw, by+bh), (0,0,255), 2)
	cv2.imshow('img',img)
	k=cv2.waitKey(30) & 0xff
	if k == 27:
		break
cap.release()
cv2.destroyAllWindows()