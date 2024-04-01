import time
import serial

arduinoData = serial.Serial('com3', 38400)
time.sleep(2)
while True:

    while arduinoData.inWaiting() == 0:
        pass

    datapacket = arduinoData.readline(11)
    #datapacket = arduinoData.readline()[:-2]
    #datapacket = str(datapacket, 'utf-8')
    #datapacket = int(datapacket)
    print(datapacket)