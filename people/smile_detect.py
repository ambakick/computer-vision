import cv2

#importing the cascade from the xml file
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
#detection functions
def detect(gray, frame):
    #x and y coordinates of the left corner
    #w and h width and height
    #cascades works in black and white images
    faces = face_cascade.detectMultiScale(gray, 1.3)
    # image, scale factor (1.3 times reduced size), 5(atleast 5 neighbour zones accepted also need to be accepted))

    #faces contains coordinates x,y,w,h
    #drawing rectangle with these cordinates
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
        roi_gray = gray[ y:y+h, x:x+w ]
        roi_color = frame[ y:y+h, x:x+w ]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 22)
        for(ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh), (0, 255, 0), 2)

        smiles = smile_cascade.detectMultiScale(roi_gray, 1.7, 22)
        for(sx, sy, sw, sh) in smiles:
            cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 0, 255), 2)
    return frame
    #as roi is a part of frame, drawing in roi will affect the frame
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    frame = cv2.flip(frame,1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #calling the function to draw rectangles
    canvas = detect(gray, frame)
    #diplaying the result in a window
    cv2.imshow('Video', canvas)
    #to interrupt the while loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#releasing video camera resource
video_capture.release()
cv2.destroyAllWindows()