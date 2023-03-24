import cv2
import numpy as np
import time
import serial
import serial.tools.list_ports
import imutils
from imutils.perspective import four_point_transform
from tensorflow.keras.models import model_from_json

def GetLabels(): 
    # 레이블 불러오기
    labels = []
    file = open("model/labels.txt", "r")
    for x in file:
      labels.append(x.rstrip('\n'))

    print('labels = ', labels)
    print()
    file.close()

    return labels 


def openSerial():
    ports = serial.tools.list_ports.comports()
    com = ''

    for port, desc, hwid in sorted(ports):        
        if 'USB' in desc:
            com = port
    if com != '':
        print('Micro:bit detected: ', com)   
    else:
        print('Please connect your microbit to this PC via USB')    
    
    ser = serial.Serial(com, 115200, timeout=0,parity=serial.PARITY_NONE, rtscts=0)  
    
    return ser

def closeSerial():
    ser.close()

# 시리얼 통신으로 컴퓨터에 연결되어 있는 마이크로비트에 명령 보내기
def SerialSendCommand(cmd, ser):
    cmd = str(cmd) 
    cmd  = cmd + '\n'
    cmd = str.encode(cmd) 
    ser.write(cmd)
    
def SerialReceiveResponse(ser):  
    ret = 1
    line = ser.readline().decode('utf-8')
    line = str(line)

    if line == "0": 
        ret = 0     
        
    return ret

def loadModel(): 
    with open('./model/model.json', 'r') as file_model:        
        model_desc = file_model.read()
        model = model_from_json(model_desc)
    model.load_weights('./model/weights.h5')
    
    return model 


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
                
            elif turn > 130:
                turn = 130
            
            tic = time.time()    
            text = str(turn)
            
    else:
        if time.time() - tic > 3:
            turn = 0 
            tic = time.time()
     
    SerialSendCommand(turn, ser)    
  
    return tic, text, turn

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

def ReadTrafficSign(cropped, model):

    input_width = 48
    input_height = 48
    
    resized_image = cv2.resize(cropped, (input_width, input_height)).astype(np.float32)
    normalized_image = resized_image / 255.0

    batch = normalized_image.reshape(1, input_height, input_width, 3)
    prediction = model.predict(batch)

    score = np.max(prediction) 
    class_id = np.argmax(prediction)

    return class_id, score



# 회전하기
def Move(moveTime, tic, turn, forward, ser):
    
    if forward == 1: 
    
        if turn == 90 or turn is None: 
            turn = 90.5

        a = turn - 90   #how far to turn (30 degrees)
        b = time.time() - tic # how much time has passed
        c = b/moveTime # % of forwardMoveTime (0-100%)
        d = int(c*a) # 
        cmd = turn - d

    else: 
        a = turn   #how far to turn (30 degrees)
        b = time.time() - tic # how much time has passed
        c = b/moveTime # % of forwardMoveTime (0-100%)
        d = int(c*a) #
        cmd = 90 + d
    
    ret = None
    SerialSendCommand(cmd, ser)
        
    if time.time() - tic > moveTime:
        ret = 1
    return ret

def Crop(frame, video_capture):
    width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH )
    height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT )

    y1 = int(height - int(height * .2))
    y2 = int(height - int(height * .0))
    cropFrame = frame[y1:y2, :]  

    return cropFrame, y1, y2, width, height