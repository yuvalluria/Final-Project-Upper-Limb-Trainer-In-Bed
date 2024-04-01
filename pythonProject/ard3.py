import time
import serial
import csv

arduinoData = serial.Serial('com3', 57600)
time.sleep(1)
cnt_success_reps=0
cnt_fail_reps=0
start_time = time.time()
set_time=30
rep_time=5
magnet_on=1
magnet_off=2
force_limit=2500
while True:
    current_time = time.time()
    elapsed_time = current_time - start_time
    while (arduinoData.inWaiting() == 0):
        pass
    datapacket=arduinoData.readline()
    datapacket=str(datapacket, 'utf-8')
    datapacket=int(datapacket)
    if datapacket > 0 and datapacket < force_limit:
        state_cmd = str(magnet_on)
        state_cmd = state_cmd + '\r'
        magnet_cmd = str(2)
        magnet_cmd = magnet_cmd + '\r'
        arduinoData.write(state_cmd.encode())
        arduinoData.write(magnet_cmd.encode())
        print(datapacket)

    if datapacket > force_limit :
        cnt_success_reps = cnt_success_reps+1
        state_cmd = str(magnet_off)
        state_cmd = state_cmd + '\r'
        magnet_cmd = str(0)
        magnet_cmd = magnet_cmd + '\r'
        arduinoData.write(state_cmd.encode())
        arduinoData.write(magnet_cmd.encode())
        print(datapacket)
        time.sleep(rep_time)
        start_time = 0

    #print(cnt_success_reps,cnt_fail_reps)
