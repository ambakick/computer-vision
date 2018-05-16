import numpy as np
import cv2

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))
while(cap.isOpened()):

    ret, frame =cap.read()
    
    if ret==True:
        #print("Hello: "+str(ret))
        gray1 = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        flipped_frame = cv2.flip(frame,1)
        #1 to flip vertically
        #0 to flip horizontally
        #-1 both
        out.write(flipped_frame)

        cv2.imshow('frame',gray1)

        if(cv2.waitKey(1)& 0xFF==ord('q')):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()