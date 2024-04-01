import time
import serial
import csv
import PySimpleGUI as sg
import threading
import time
import serial


# Initialize variables
cnt_success_reps = 0
cnt_fail_sets = 0

set_time = 30
rep_time = 3
magnet_on = b'\x01'
magnet_off = b'\x02'
magnet_weight = b'\x05'
force_limit = 2530
set_amount = 3
rep_amount = 4
cnt_sets = 1
cnt_reps = 1
arduinoData = serial.Serial('com3', 38400)

time.sleep(2)
start_time = time.time()
while True:

    while arduinoData.inWaiting() == 0:
        pass

    datapacket = arduinoData.readline()
    # datapacket = arduinoData.readline()[:-2]
    datapacket = str(datapacket, 'utf-8')
    datapacket = int(datapacket)
    arduinoData.reset_input_buffer()
    print(datapacket)
    if cnt_sets <= set_amount :
        if datapacket > 0 and datapacket < force_limit:
            data=magnet_on + magnet_weight
            arduinoData.write(data)
            time.sleep(10 / 1000)
            current_time = time.time()
            elapsed_time = int(current_time - start_time) % 60

            if elapsed_time >= rep_time:
                data = magnet_off + b'\x00'
                arduinoData.write(data)
                time.sleep(10 / 1000)
                cnt_fail_sets += 1
                start_time = current_time
                #print(cnt_fail_sets)
                i = 0
                while i < set_time / 3:
                    time.sleep(1)
                    i = i + 1
                    time_delay = int(time.time() - start_time)
                    print('errored set, waiting to new set, {:02d}:{:02d}:{:02d}'.format(time_delay // 3600,
                                                                                         (time_delay % 3600 // 60),
                                                                                         time_delay % 60))
                print("failed in set {} rep {}".format(cnt_sets, cnt_reps))
                cnt_sets = cnt_sets + 1
                cnt_reps = 1
                data = magnet_on + magnet_weight
                arduinoData.write(data)
                time.sleep(10 / 1000)
                current_time = 0
                start_time = time.time()

        if datapacket > force_limit:
            data = magnet_off + b'\x00'
            arduinoData.write(data)
            time.sleep(10 / 1000)
            print(datapacket)
            i = 0
            while i < rep_time:
                time.sleep(1)
                i = i + 1
                time_delay = int(time.time() - start_time)
                print('rep {} finished .waiting: {:02d}:{:02d}:{:02d}'.format(cnt_reps, time_delay // 3600,
                                                                             (time_delay % 3600 // 60),
                                                                             time_delay % 60))
            if cnt_reps < rep_amount :
                cnt_reps = cnt_reps + 1
                #print(cnt_reps)
            elif cnt_reps == rep_amount :

                #print(cnt_sets)

                i = 0
                start_time=time.time()
                while i < set_time / 3:
                    time.sleep(1)
                    i = i + 1
                    time_delay = int(time.time() - start_time)
                    print('set {} finished waiting:, {:02d}:{:02d}:{:02d}'.format(cnt_sets,time_delay // 3600,
                                                                               (time_delay % 3600 // 60),
                                                                               time_delay % 60))
                cnt_sets = cnt_sets + 1
                cnt_reps = 1
            start_time = time.time()
            cnt_success_reps += 1
            arduinoData.reset_input_buffer()

    elif cnt_sets > set_amount :
        print('total reps achieved {} from {}'.format(cnt_success_reps, rep_amount * set_amount))
        break

