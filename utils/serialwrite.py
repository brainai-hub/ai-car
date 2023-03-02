import serial
import serial.tools.list_ports

def startSerial():
    
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
    
    return com, ser

def closeSerial(ser):
    
    try:
        ser.close()
        
    except:
        pass

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
