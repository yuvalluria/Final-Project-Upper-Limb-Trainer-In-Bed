import time
import serial
import csv

arduinoData = serial.Serial('com3', 38400)
cnt_success_reps = 0
cnt_fail_sets = 0
start_time = time.time()
set_time = 30
rep_time = 10
magnet_on = 1
magnet_off = 2
force_limit = 2530
set_amount = 3
rep_amount = 8
cnt_sets = 1
cnt_reps = 1
time.sleep(2)
while True:

    while arduinoData.inWaiting() == 0:
        pass

    datapacket = arduinoData.readline()
    # datapacket = arduinoData.readline()[:-2]
    datapacket = str(datapacket, 'utf-8')
    datapacket = int(datapacket)
    arduinoData.reset_input_buffer()
    print(datapacket)
    if cnt_sets < set_amount + 1:
        if datapacket > 0 and datapacket < force_limit:
            state_cmd = str(magnet_on) + '\r'
            arduinoData.write(state_cmd.encode())
            time.sleep(10 / 1000)
            weight_cmd = str(2) + '\r'
            arduinoData.write(weight_cmd.encode())
            time.sleep(10 / 1000)
            current_time = time.time()
            elapsed_time = int(current_time - start_time) % 60

            if elapsed_time >= rep_time:
                state_cmd = str(magnet_off) + '\r'
                arduinoData.write(state_cmd.encode())
                time.sleep(10 / 1000)
                cnt_fail_sets += 1
                start_time = current_time
                print(cnt_fail_sets)
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
                cnt_reps = 0
                state_cmd = str(magnet_on) + '\r'
                arduinoData.write(state_cmd.encode())  # Turn on magnet again
                time.sleep(10 / 1000)
                current_time = 0
                start_time = time.time()

        if datapacket > force_limit:
            state_cmd = str(magnet_off) + '\r'
            arduinoData.write(state_cmd.encode())
            time.sleep(10 / 1000)
            print(datapacket)
            i = 0
            while i < rep_time:
                time.sleep(1)
                i = i + 1
                time_delay = int(time.time() - start_time)
                print('rep finished {}.waiting: {:02d}:{:02d}:{:02d}'.format(cnt_reps, time_delay // 3600,
                                                                             (time_delay % 3600 // 60),
                                                                             time_delay % 60))
            if cnt_reps < rep_amount + 1:
                cnt_reps = cnt_reps + 1
                print(cnt_reps)
            elif cnt_reps == rep_amount + 1:
                cnt_sets = cnt_sets + 1
                print(cnt_sets)
                cnt_reps = 1
                i = 0
                while i < set_time / 3:
                    time.sleep(1)
                    i = i + 1
                    time_delay = int(time.time() - start_time)
                    print('set finished waiting:, {:02d}:{:02d}:{:02d}'.format(time_delay // 3600,
                                                                               (time_delay % 3600 // 60),
                                                                               time_delay % 60))
            start_time = time.time()
            cnt_success_reps += 1

    elif cnt_sets == set_amount + 1:
        print('total reps achieved {} from {}'.format(cnt_success_reps, rep_amount * set_amount))
        break


