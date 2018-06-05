import cv2
import numpy as np
import dlib

#Update all the trackers and remove the ones for which the update
#indicated the quality was not good enough
fidsToDelete = []  
for fid in faceTrackers.keys():  
    trackingQuality = faceTrackers[ fid ].update( baseImage )

    #If the tracking quality is good enough, we must delete
    #this tracker
    if trackingQuality < 7:
        fidsToDelete.append( fid )

for fid in fidsToDelete:  
    print("Removing tracker " + str(fid) + " from list of trackers")
    faceTrackers.pop( fid , None )
#Now use the haar cascade detector to find all faces
#in the image
faces = faceCascade.detectMultiScale(gray, 1.3, 5)

#Loop over all faces and check if the area for this
#face is the largest so far
#We need to convert it to int here because of the
#requirement of the dlib tracker. If we omit the cast to
#int here, you will get cast errors since the detector
#returns numpy.int32 and the tracker requires an int
for (_x,_y,_w,_h) in faces:  
    x = int(_x)
    y = int(_y)
    w = int(_w)
    h = int(_h)

    #calculate the centerpoint
    x_bar = x + 0.5 * w
    y_bar = y + 0.5 * h

    #Variable holding information which faceid we 
    #matched with
    matchedFid = None

    #Now loop over all the trackers and check if the 
    #centerpoint of the face is within the box of a 
    #tracker
    for fid in faceTrackers.keys():
        tracked_position =  faceTrackers[fid].get_position()

        t_x = int(tracked_position.left())
        t_y = int(tracked_position.top())
        t_w = int(tracked_position.width())
        t_h = int(tracked_position.height())

        #calculate the centerpoint
        t_x_bar = t_x + 0.5 * t_w
        t_y_bar = t_y + 0.5 * t_h

        #check if the centerpoint of the face is within the 
        #rectangleof a tracker region. Also, the centerpoint
        #of the tracker region must be within the region 
        #detected as a face. If both of these conditions hold
        #we have a match
        if ( ( t_x <= x_bar   <= (t_x + t_w)) and 
             ( t_y <= y_bar   <= (t_y + t_h)) and 
             ( x   <= t_x_bar <= (x   + w  )) and 
             ( y   <= t_y_bar <= (y   + h  ))):
            matchedFid = fid

    #If no matched fid, then we have to create a new tracker
    if matchedFid is None:
        print("Creating new tracker " + str(currentFaceID))
        #Create and store the tracker 
        tracker = dlib.correlation_tracker()
        tracker.start_track(baseImage,
                            dlib.rectangle( x-10,
                                            y-20,
                                            x+w+10,
                                            y+h+20))

        faceTrackers[ currentFaceID ] = tracker

        #Increase the currentFaceID counter
        currentFaceID += 1

#Now loop over all the trackers we have and draw the rectangle
#around the detected faces. If we 'know' the name for this person
#(i.e. the recognition thread is finished), we print the name
#of the person, otherwise the message indicating we are detecting
#the name of the person
for fid in faceTrackers.keys():  
    tracked_position =  faceTrackers[fid].get_position()

    t_x = int(tracked_position.left())
    t_y = int(tracked_position.top())
    t_w = int(tracked_position.width())
    t_h = int(tracked_position.height())

    cv2.rectangle(resultImage, (t_x, t_y),
                            (t_x + t_w , t_y + t_h),
                            rectangleColor ,2)

    #If we do have a name for this faceID already, we print the name
    if fid in faceNames.keys():
        cv2.putText(resultImage, faceNames[fid] , 
                    (int(t_x + t_w/2), int(t_y)), 
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 2)
    else:
        cv2.putText(resultImage, "Detecting..." , 
                    (int(t_x + t_w/2), int(t_y)), 
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 2)
