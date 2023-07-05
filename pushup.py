import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_drawing_styles=mp.solutions.drawing_styles

def push():
    count=0
    position=None
    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
        while cap.isOpened():
            success,image=cap.read()
            if not success:
                print("Empty Camera")
                break
                
    #         # Recolor image to RGB
    #         image = cv2.cvtColor(cv2.flip(image,1), cv2.COLOR_BGR2RGB)
            
    #         # Make detection
    #         result = pose.process(image)
            
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            result = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            imlist=[]
            
            if result.pose_landmarks:
                mp_drawing.draw_landmarks(
                image,result.pose_landmarks,mp_pose.POSE_CONNECTIONS)
                for id,im in enumerate(result.pose_landmarks.landmark):
                    h,w,_=image.shape
                    X,Y=int(im.x*w),int(im.y*h)
                    imlist.append([id,X,Y])
            if len(imlist)!=0:      
                if ((imlist[12][2] - imlist[14][2])>=-100 and (imlist[11][2] - imlist[13][2])>=-100):
                    position = "down"
                
                if ((imlist[12][2] - imlist[14][2])<=-100 and (imlist[11][2] - imlist[13][2])<=-100) and position == "down":
                    position = "up"
                    count +=1 
                    print(count)
                    
                # Render curl counter
                # Setup status box
                cv2.rectangle(image, (0,0), (200,73), (255,255,255), -1)
                cv2.putText(image, 'Num Pushups', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,153,0), 1, cv2.LINE_AA)
                cv2.putText(image, str(count),
                        (30,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
                
    #         cv2.imshow("Push up counter",cv2.flip(image,1))
            resized = cv2.resize(image, (1200,850), interpolation = cv2.INTER_AREA)
            cv2.imshow("Push up counter",resized)
            key=cv2.waitKey(1)
            if key==ord('q'):
                break
            
    cap.release()
    cv2.destroyAllWindows()