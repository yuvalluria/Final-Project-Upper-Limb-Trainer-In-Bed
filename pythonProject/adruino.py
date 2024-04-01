import time
import serial
import csv

arduinoData = serial.Serial('com3', 57600)
time.sleep(1)

while True:
    while (arduinoData.inWaiting() == 0):
        pass
    datapacket=arduinoData.readline()
    datapacket=str(datapacket, 'utf-8')
    datapacket=int(datapacket)
    if datapacket > 0 and datapacket < 2500:
        cmd = str(1)
        cmd = cmd + '\r'
        arduinoData.write(cmd.encode())
        print(datapacket)
    elif datapacket > 2500 :
        cmd = str(2)
        cmd = cmd + '\r'
        arduinoData.write(cmd.encode())
        time.sleep(1)
        print(datapacket)



