import cv2

video_capture = cv2.VideoCapture('TownCentreXVID.avi')
#video_capture.set(video_capture, CAP_PROP_FPS, 30)
video_capture.set(cv2.CAP_PROP_FPS, 40)
i=0
j=0
while (video_capture.isOpened()):
    ret, frame = video_capture.read()
    cv2.imwrite("Pictures%d.jpg" % (i+1),frame)
    i=i+1
    if i==1500:
        break
print("finished")
