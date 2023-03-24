import cv2
import numpy as np
import time

import imutils
from imutils.perspective import four_point_transform
from tensorflow.keras.models import model_from_json

 

#교통 신호 찾기
def FindTrafficSign(frame):

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

def ReadTrafficSign(cropped, model, labels):
    input_width = 48
    input_height = 48
    
    resized_image = cv2.resize(cropped, (input_width, input_height)).astype(np.float32)
    normalized_image = resized_image / 255.0

    batch = normalized_image.reshape(1, input_height, input_width, 3)
    prediction = model.predict(batch, verbose = 0)

    score = np.max(prediction) 
    class_id = np.argmax(prediction)
    text = labels[class_id] + ' ' + str('%.0f' % (score*100)) + '%' 

    return class_id, score, text

# 회전하기
def Move(moveTime, tic, turn, forward):
    
    if forward == True: 
    
        if turn == 90 or turn is None: 
            turn = 90.5
    
        time_elapsed = time.time() - tic
        time_remaining = moveTime - time_elapsed
        divisor = moveTime / time_remaining

        turn = turn - 90
        angle = turn/divisor
        cmd = int(90 + angle)

    else: 
        
        time_elapsed = time.time() - tic                              # how much time has passed
        time_percent = time_elapsed/moveTime                                   # % of MoveTime (0-100%)
        
        move_percent = int(time_percent*turn)                
        cmd = 90 + move_percent                
       
    ret = None
        
    if time.time() - tic > moveTime:
        ret = 1
    return ret, cmd