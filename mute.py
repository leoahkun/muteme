#!/usr/bin/env python

import cv2
import sys
from mtcnn.mtcnn import MTCNN
import subprocess
import tensorflow as tf
from detector import TSDetector
from boxoccupied import *

#run apple script
def asrun(ascript):
    proc = subprocess.Popen(['osascript', '-'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,encoding='utf8') 
    stdout_output = proc.communicate(ascript)[0]
    print(stdout_output)

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
detector = MTCNN()
handsDetector = TSDetector()

video_capture = cv2.VideoCapture(0) #set index of webcam.

asrun("set volume input volume 100") #unmute
hand_over_mouth = False
unmute_buffer_threshold = 8
unmute_buffer_count = 0

muted = False

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,15)
fontScale              = 0.5
lineType               = 2

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    if ret==True:
        frame = cv2.resize(frame, (320,180), interpolation=cv2.INTER_CUBIC)
        process_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)        
        
        faces_dnn = detector.detect_faces(process_frame)    
        hands = handsDetector.detect(process_frame)
        
        num_faces = len(faces_dnn)        
        new_hand_over_mouth = False
        if num_faces > 0:
            box = faces_dnn[0]["box"]
            bx = box[0]
            by = box[1]
            bw = box[2]
            bh = box[3]                        
            face_box = faces_dnn[0]

            for (hx, hy, hw, hh) in hands:
                if box_occupied((bx,by),(bx+bw,by+bh),(hx,hy),(hx+hw,hy+hh)):
                    new_hand_over_mouth = True
        
        if new_hand_over_mouth:
            unmute_buffer_count = 0

        if hand_over_mouth != new_hand_over_mouth:            
            if new_hand_over_mouth:
                print("MUTE!!!!")
                asrun("set volume input volume 0")                
                muted = True
                hand_over_mouth = new_hand_over_mouth
            else:
                unmute_buffer_count = unmute_buffer_count+1  
                # print("unmute count",unmute_buffer_count)
                if unmute_buffer_count >= unmute_buffer_threshold:
                    print("unmute...")
                    muted = False
                    asrun("set volume input volume 100")    
                    hand_over_mouth = new_hand_over_mouth                  

        # draw
        for face in faces_dnn:
            box = face["box"]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)            

        for (x, y, w, h) in hands:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

        if muted:
            cv2.putText(frame,"Muted!", 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                (0,0,255),
                lineType)
        else:
            cv2.putText(frame,"Listening", 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                (0,255,0),
                lineType)

        # Display the output
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
