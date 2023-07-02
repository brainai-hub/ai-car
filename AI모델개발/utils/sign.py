import cv2
import numpy as np
import time

import imutils
from imutils.perspective import four_point_transform
from tensorflow.keras.models import model_from_json

def FindTrafficSign(frame):              #교통 신호 찾기 함수 정의

    frameArea = frame.shape[0] * frame.shape[1]
    cropped = None
    box = None
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (85,100,100), (115,255,255))

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts) > 0:
        c = max(cnts, key = cv2.contourArea)  
        area = cv2.contourArea(c) 
        
        if area > frameArea * 0.005:
            box = cv2.minAreaRect(c)  
            box = cv2.boxPoints(box)
            box = np.int0(box)    
            cropped = four_point_transform(frame, [box][0]) 

    return cropped, box
