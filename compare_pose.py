import cv2
import mediapipe as mp
import numpy as np
import time
import datetime
import matplotlib.pyplot as plt
# import pyshine as ps
from calc_angle import calculateAngle
from extract_keypoints import extractKeypoint
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def compare_pose(image,angle_point,angle_user, angle_target):
    angle_user = np.array(angle_user)
    angle_target = np.array(angle_target)
    angle_point = np.array(angle_point)
    stage = 0
    cv2.rectangle(image,(0,0), (370,40), (255,255,255), -1)
    cv2.putText(image, str("Score:"), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
    height, width, _ = image.shape   
    
    if angle_user[0] < (angle_target[0] - 20):
        stage = stage + 1
        cv2.circle(image,(int(angle_point[0][0]*width), int(angle_point[0][1]*height)),30,(0,0,255),5) 
        
    if angle_user[0] > (angle_target[0] + 20):
        stage = stage + 1
        cv2.circle(image,(int(angle_point[0][0]*width), int(angle_point[0][1]*height)),30,(0,0,255),5)

        
    if angle_user[1] < (angle_target[1] -20):
        stage = stage + 1
        cv2.circle(image,(int(angle_point[1][0]*width), int(angle_point[1][1]*height)),30,(0,0,255),5)
        
    if angle_user[1] >(angle_target[1] + 20):
        stage = stage + 1
        cv2.circle(image,(int(angle_point[1][0]*width), int(angle_point[1][1]*height)),30,(0,0,255),5)

        
    if angle_user[2] < (angle_target[2] - 20):
        stage = stage + 1
        cv2.circle(image,(int(angle_point[2][0]*width), int(angle_point[2][1]*height)),30,(0,0,255),5)

    if angle_user[2] > (angle_target[2] + 20):
        stage = stage + 1
        cv2.circle(image,(int(angle_point[2][0]*width), int(angle_point[2][1]*height)),30,(0,0,255),5)

    if angle_user[3] < (angle_target[3] - 20):
        stage = stage + 1
        cv2.circle(image,(int(angle_point[3][0]*width), int(angle_point[3][1]*height)),30,(0,0,255),5)

    if angle_user[3] > (angle_target[3] + 20):
        stage = stage + 1
        cv2.circle(image,(int(angle_point[3][0]*width), int(angle_point[3][1]*height)),30,(0,0,255),5)

    if angle_user[4] < (angle_target[4] - 20):
        stage = stage + 1
        cv2.circle(image,(int(angle_point[4][0]*width), int(angle_point[4][1]*height)),30,(0,0,255),5)

    if angle_user[4] > (angle_target[4] + 20):
        stage = stage + 1
        cv2.circle(image,(int(angle_point[4][0]*width), int(angle_point[4][1]*height)),30,(0,0,255),5)

    if angle_user[5] < (angle_target[5] - 20):
        stage = stage + 1
        cv2.circle(image,(int(angle_point[5][0]*width), int(angle_point[5][1]*height)),30,(0,0,255),5)
        

    if angle_user[5] > (angle_target[5] + 20):
        stage = stage + 1
        cv2.circle(image,(int(angle_point[5][0]*width), int(angle_point[5][1]*height)),30,(0,0,255),5)

    if angle_user[6] < (angle_target[6] - 20):
        stage = stage + 1
        cv2.circle(image,(int(angle_point[6][0]*width), int(angle_point[6][1]*height)),30,(0,0,255),5)
        

    if angle_user[6] > (angle_target[6] + 20):
        stage = stage + 1
        cv2.circle(image,(int(angle_point[6][0]*width), int(angle_point[6][1]*height)),30,(0,0,255),5)


    if angle_user[7] < (angle_target[7] - 20):
        stage = stage + 1
        cv2.circle(image,(int(angle_point[7][0]*width), int(angle_point[7][1]*height)),30,(0,0,255),5)

    if angle_user[7] > (angle_target[7] + 20):
        stage = stage + 1
        cv2.circle(image,(int(angle_point[7][0]*width), int(angle_point[7][1]*height)),30,(0,0,255),5)
    
    if stage!=0:
        #print("FIGHTING!")
        cv2.putText(image, str("FIGHTING!"), (170,30), cv2.FONT_HERSHEY_SIMPLEX, 1, [0,0,255], 2, cv2.LINE_AA)
        
        pass
    else:
        #print("PERFECT")
        cv2.putText(image, str("PERFECT"), (170,30), cv2.FONT_HERSHEY_SIMPLEX, 1, [0,0,255], 2, cv2.LINE_AA)
    return stage