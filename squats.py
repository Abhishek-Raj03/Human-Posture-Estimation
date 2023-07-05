import cv2
import mediapipe as mp
import time
import numpy as np
# import pandas as pd
import datetime
import math
from calc_angle import calculateAngle
# from celluloid import Camera
# import pyshine as ps
# from calc_angle import calculateAngle,Average,convert_data,dif_compare,diff_compare_angle
# from extract_keypoints import extractKeypoint
# from compare_pose import compare_pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# def calculate_angle(a,b,c):
#     a = np.array(a) # First
#     b = np.array(b) # Mid
#     c = np.array(c) # End
    
#     radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
#     angle = np.abs(radians*180.0/np.pi)
    
#     if angle >180.0:
#         angle = 360-angle
        
#     return angle

def squats_fun():
    cap = cv2.VideoCapture(0)

    # Curl counter variables
    counter = 0 
    stage = None

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                # shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                # elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                # wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                angle_point=[]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                angle_point.append(right_elbow)
                
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                angle_point.append(left_elbow)
                
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                angle_point.append(right_shoulder)
                
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                angle_point.append(left_shoulder)
                
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                        
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                angle_point.append(right_hip)
                
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                angle_point.append(left_hip)
                
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                angle_point.append(right_knee)
                
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                angle_point.append(left_knee)
                right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                
                angle = []
                
                r_elbow = calculateAngle(right_shoulder, right_elbow, right_wrist)
                angle.append(int(r_elbow))
                l_elbow = calculateAngle(left_shoulder, left_elbow, left_wrist)
                angle.append(int(l_elbow))
                r_shoulder = calculateAngle(right_elbow, right_shoulder, right_hip)
                angle.append(int(r_shoulder))
                l_shoulder = calculateAngle(left_elbow, left_shoulder, left_hip)
                angle.append(int(l_shoulder))
                r_hip = calculateAngle(right_shoulder, right_hip, right_knee)
                angle.append(int(r_hip))
                l_hip = calculateAngle(left_shoulder, left_hip, left_knee)
                angle.append(int(l_hip))
                r_knee = calculateAngle(right_hip, right_knee, right_ankle)
                angle.append(int(r_knee))
                l_knee = calculateAngle(left_hip, left_knee, left_ankle)
                angle.append(int(l_knee))

                # Get coordinates
                # nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,landmarks[mp_pose.PoseLandmark.NOSE.value].y]
                # right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                # left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                # right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                # left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                
                # Calculate angle
                # angle_right = np.abs(calculateAngle(right_hip, right_knee, nose))
                # angle_left = np.abs(calculateAngle(left_hip, left_knee, nose))
                
                # Visualize angle
                # cv2.putText(image, "Right: " + str(angle_right), 
                #             tuple(np.multiply(right_knee, [640, 480]).astype(int)), 
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                
                # cv2.putText(image, "Left: " + str(angle_left), 
                #             tuple(np.multiply(left_knee, [640, 480]).astype(int)), 
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                
                # Squat counter logic
                if l_elbow>140 and r_elbow>140 and l_shoulder>30 and r_shoulder>30:
                    if l_knee < 160 and r_knee < 160:
                        stage = "down"
                    if (l_knee > 170 and r_knee > 170) and stage =='down':
                        stage="up"
                        counter +=1
                        # print(counter)

                # Calculate angle
                # angle = calculate_angle(shoulder, elbow, wrist)
                
                # Visualize angle
                # cv2.putText(image, str(angle), 
                #             tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                #                     )
                
                # # Curl counter logic
                # if angle > 160:
                #     stage = "down"
                # if angle < 30 and stage =='down':
                #     stage="up"
                #     counter +=1
                    # print(counter)
                    
                
                        
            except:
                cv2.putText(image, "Warning! No pose detected", (150,200), cv2.FONT_HERSHEY_SIMPLEX, 1, [0,0,255], 2, cv2.LINE_AA)
                pass
            
            # Render curl counter
            # Setup status box
            cv2.rectangle(image, (0,0), (200,73), (255,255,255), -1)
            
            # Rep data
            cv2.putText(image, 'count', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,153,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter),
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            
            # Stage data
            cv2.putText(image, 'STAGE', (80,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,153,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (70,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            
                    
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            
            resized = cv2.resize(image, (1200,850), interpolation = cv2.INTER_AREA)
            cv2.imshow('count curls', resized)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()