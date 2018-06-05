import cv2
import sys
 
#(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')￼
 
if __name__ == '__main__' :
 
    # Set up tracker.
    # Instead of MIL, you can also use
 
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
    tracker_type = tracker_types[2]
 

    face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # if int(minor_ver) < 3:
    #     tracker = cv2.Tracker_create(tracker_type)
    # else:
    if tracker_type == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
        tracker3 = cv2.TrackerBoosting_create()
    if tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
        tracker3 = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
        tracker3 = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
        tracker3 = cv2.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
        tracker3 = cv2.TrackerMedianFlow_create()
    if tracker_type == 'GOTURN':
        tracker = cv2.TrackerGOTURN_create()
        tracker3 = cv2.TrackerGOTURN_create()
 
    # Read video
    video = cv2.VideoCapture(0)
 
    # Exit if video not opened.
    if not video.isOpened():
        print ("Could not open video")
        sys.exit()
 
    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()
     
    # Define an initial bounding box
    #bbox = (287, 23, 86, 320)
 
    # Uncomment the line below to select a different bounding box
    #bbox = cv2.selectROI(frame, False)
 
    # Initialize tracker with first frame and bounding box
    faces = []
    while len(faces)==0:
        ok, frame = video.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(gray,1.3,5)
    id=0
    #print (type(faces))
    #print  (faces.shape)
    # bbox[0] = int(faces[0][0])
    # bbox[1] = faces[0][1]
    # bbox[2] = faces[0][2]
    # bbox[3] = faces[0][3]
    bbox = tuple(faces[0])
    #print (str(faces[0][0])+str(bbox[0])+str(faces[0][1])+str(bbox[1]))
	# for(x,y,w,h) in faces:
    #     cv2.rectangle(img,(x,y),(x+w,y+h),	(255,0,0),2)
	# 	roi_gray=gray[y:y+h,x:x+w]
	# 	roi_color= img[y:y+h,x:x+w]
	# 	id=id+1
	# 	# eyes=eye_cascade.detectMultiScale(roi_gray)
	# 	cv2.putText(roi_color, str(id), (10,20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0,0,250), 1, cv2.LINE_AA)
		# for(ex,ey,ew,eh) in eyes:
		# 	cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
		# 	roi_gray=gray[ey:ey+eh,ex:ex+ew]
		# 	roi_color= img[ey:ey+eh,ex:ex+ew]
    print ( type(bbox))
    print("hi"+str(bbox))
    ok = tracker.init(frame, bbox)  

    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
         
        # Start timer
        timer = cv2.getTickCount()
 
        # Update tracker
        ok, bbox = tracker.update(frame)
 
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
 
        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
     
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
 
        # Display result
        cv2.imshow("Tracking", frame)
 
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break