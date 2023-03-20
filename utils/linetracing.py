import cv2
import numpy as np
import time

# 검정색 도로 라인 따라 주행하기
def LineTracing(threshold, sens, cropFrame, frame, tic, width, height, y1, ser):
    
    text = "No line"
    turn = None
    
    gray = cv2.cvtColor(cropFrame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    ret, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY_INV)
    
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, 
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    if len(cnts) > 0:
        
        c = max(cnts, key=cv2.contourArea)
        M = cv2.moments(c)

        if M['m00'] == 0:
            pass

        else:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            
            cv2.line(frame,(cx,0), (cx, int(height)), (255, 0 , 0), 1)
            cv2.line(frame,(0,cy + y1), (int(width), cy + y1), (255, 0, 0), 1)
            cv2.drawContours(frame, cnts, -1, (0, 0 , 255), 1, offset = (0,y1))
                        
            turn = cx / width*100
            turn = turn - 50
            turn = turn * sens
            turn = turn - 90
            turn = abs(int(turn))
                    
            if turn < 40:
                turn = 40
                
            elif turn > 140:
                turn = 140
            
            tic = time.time()    
            text = str(turn)
            
    else:
        if time.time() - tic > 3:
            turn = 0 
            tic = time.time()
  
    return tic, text, turn, thresh

# 빨간색 배경의 횡단보도 찾기
def RedDetection(cropFrame, y1):

    box = None
    frameArea = cropFrame.shape[0] * cropFrame.shape[1]
    
    hsv = cv2.cvtColor(cropFrame, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, (0, 50, 50), (10, 255,255))
    mask2 = cv2.inRange(hsv, (170, 50, 50), (179, 255,255))
    mask = mask1 + mask2
    
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts) > 0:
        
        c = max(cnts, key = cv2.contourArea) 
        area = cv2.contourArea(c)  

        if area > frameArea * 0.05:
            
            box = cv2.minAreaRect(c)  
            box = cv2.boxPoints(box)
            box = np.int0(box)
            box = box + [0, y1]
            
    return box
