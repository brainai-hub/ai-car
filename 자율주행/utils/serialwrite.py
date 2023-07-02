import serial
import serial.tools.list_ports
import sys

def startSerial(serial_on):
    ser = None
    if serial_on == True:
        ports = serial.tools.list_ports.comports()
        com = ''
        print('\n -- Microbit --')
        for port, desc, hwid in sorted(ports):
            if 'USB' in desc:
                com = port
        if com != '':
            print('Microbit USB detected: ', com)
            ser = serial.Serial(com, 115200, 
                                timeout=0, 
                                parity=serial.PARITY_NONE, 
                                rtscts=0) 
        else:
            print('No Microbit USB detected')
            sys.exit()
    return ser

# 시리얼 통신으로 컴퓨터에 연결되어 있는 마이크로비트에 명령 보내기
def SerialSendCommand(cmd, ser, serial_on):
    if serial_on == True:
        cmd = str(cmd) 
        cmd  = cmd + '\n'
        cmd = str.encode(cmd) 
        ser.write(cmd)

def SerialReceiveResponse(ser, serial_on):  
    ret = 0 
    if serial_on == True:
        ret = 1
        line = ser.readline().decode('utf-8')
        line = str(line)

        if line == "0": 
            ret = 0     
    return ret

def closeSerial(ser, serial_on):
    if serial_on == True:
        try:
            ser.close()
        except:
            pass
