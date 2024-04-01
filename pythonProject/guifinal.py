from csv import writer
import PySimpleGUI as sg
import serial
from physiotherapist import physiotherapist
import matplotlib.pyplot as plt
import pandas as pd
import time

df_of_patients = pd.read_csv("patients.csv")
pd_of_physios = pd.read_csv("physiotherapists.csv")
df_of_plans = pd.read_csv("assigned_plans.csv")
df_of_rehab_plans = pd.read_csv("rehab_plans.csv")
df_of_future_plans = pd.read_csv("Assigned plans before completed.csv")
cnt_success_reps = 0
cnt_fail_sets = 0
start_time = time.time()
set_time = 30
rep_time = 5
magnet_on = b'\x01'
magnet_off = b'\x02'
magnet_weight = b'\x05'
force_limit = 2530
set_amount = 3
rep_amount = 8
cnt_sets = 1
cnt_reps = 1
sg.theme('DarkBlue')


def open_window_session():
    # Define the layout of the window
    layout = [
        [
            sg.Column(
                [[sg.Text("Num of reps", size=(25, 2), font=("Helvetica", 20, "bold"))],
                 [sg.Text(key='Num of reps', size=(25, 2), font=("Helvetica", 20, "bold"))],
                 [sg.Text("Num of sets", size=(25, 2), font=("Helvetica", 20, "bold"))],
                 [sg.Text(key='Num of sets', size=(25, 2), font=("Helvetica", 20, "bold"))],
                 [sg.Text(key='output', size=(25, 2), font=("Helvetica", 20, "bold"))],
                    [sg.Button("Start", key="-START-", size=(25, 2), font=("Helvetica", 20, "bold"))],
                    [sg.Button("Stop", key="-STOP-", size=(25, 2), font=("Helvetica", 20, "bold"))],
                    [sg.Button("Exit", key="-EXIT-", size=(25, 2), font=("Helvetica", 20, "bold"))],
                ],
                element_justification="right",
                vertical_alignment="top",  # Align to the top of the column
                expand_y=True,  # Expand vertically to fill the availableטאתצל space
            ),
            sg.Image(filename="workout.PNG", pad=(20, 20)),  # Add padding to the image
        ],
    ]

    window = sg.Window("Session window", layout, finalize=True)
    window.maximize()
    event, values = window.read()
    print = sg.EasyPrint
    while True:
        window['Num of sets'].update(cnt_sets)
        window['Num of reps'].update(cnt_reps)
        if event == "-START-":
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
            start_time=time.time()
            while True:

                while arduinoData.inWaiting() == 0:
                    pass

                datapacket = arduinoData.readline()
                # datapacket = arduinoData.readline()[:-2]
                datapacket = str(datapacket, 'utf-8')
                datapacket = int(datapacket)
                arduinoData.reset_input_buffer()
                #print(datapacket)
                if cnt_sets <= set_amount:
                    if datapacket > 0 and datapacket < force_limit:
                        data = magnet_on + magnet_weight
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
                            # print(cnt_fail_sets)
                            i = 0
                            while i < set_time / 3:
                                time.sleep(1)
                                i = i + 1
                                time_delay = int(time.time() - start_time)
                                window['output'].update('errored set, waiting to new set, {:02d}:{:02d}:{:02d}'.format(time_delay // 3600,
                                                                                                     (
                                                                                                                 time_delay % 3600 // 60),
                                                                                                     time_delay % 60))
                            window['output'].update("failed in set {} rep {}".format(cnt_sets, cnt_reps))
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
                        #print(datapacket)
                        i = 0
                        while i < rep_time:
                            time.sleep(1)
                            i = i + 1
                            time_delay = int(time.time() - start_time)
                            window['output'].update('rep {} finished .waiting: {:02d}:{:02d}:{:02d}'.format(cnt_reps, time_delay // 3600,
                                                                                          (time_delay % 3600 // 60),
                                                                                          time_delay % 60))
                        if cnt_reps < rep_amount:
                            cnt_reps = cnt_reps + 1
                            # print(cnt_reps)
                        elif cnt_reps == rep_amount:

                            # print(cnt_sets)

                            i = 0
                            start_time = time.time()
                            while i < set_time / 3:
                                time.sleep(1)
                                i = i + 1
                                time_delay = int(time.time() - start_time)
                                window['output'].update('set {} finished waiting:, {:02d}:{:02d}:{:02d}'.format(cnt_sets,
                                                                                              time_delay // 3600,
                                                                                              (time_delay % 3600 // 60),
                                                                                              time_delay % 60))
                            cnt_sets = cnt_sets + 1
                            cnt_reps = 1
                        start_time = time.time()
                        cnt_success_reps += 1
                        arduinoData.reset_input_buffer()

                elif cnt_sets > set_amount:
                    window['output'].update('total reps achieved {} from {}'.format(cnt_success_reps, rep_amount * set_amount))
                    break

        if event == "-EXIT-" or event == sg.WINDOW_CLOSED:
            break

    window.close()


def register_window_physio():
    layout7 = [
        [sg.Text('Pls fill out the fields:', size=(25, 2), font=("Helvetica", 20, "bold"))],
        [sg.Text("Physiotherapist_id", size=(25, 2), font=("Helvetica", 20, "bold"))],
        [sg.InputText(key='Physiotherapist_id', size=(25, 2), font=("Helvetica", 20, "bold"))],
        [sg.Text("Physiotherapist_name", size=(25, 2), font=("Helvetica", 20, "bold"))],
        [sg.InputText(key='Physiotherapist_name', size=(25, 3), font=("Helvetica", 20, "bold"))],
        [sg.B('Register', size=(25, 3), font=("Helvetica", 20, "bold"))],
        [sg.B('Clear', size=(25, 3), font=("Helvetica", 20, "bold"))],
        [sg.B('Exit', size=(25, 3), font=("Helvetica", 20, "bold"))],
    ]

    window7 = sg.Window("register physio Window", layout7, modal=True)
    while True:
        event, values = window7.read()
        # new_physiotherapist = physiotherapist(int(values['Physiotherapist_id']), values["Physiotherapist_name"])
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == 'Register':
            for i in range(len(pd_of_physios)):
                if values['Physiotherapist_id'] == pd_of_physios.loc[i, 'Physiotherapist_id']:
                    sg.popup("this id is already in use, please use a new one", font=("Helvetica", 20, "bold"))
                    break
            else:
                row = [int(values['Physiotherapist_id']), values["Physiotherapist_name"]]
                with open('physiotherapists.csv', 'a', newline='') as f_object:
                    writer_object = writer(f_object)
                    writer_object.writerow(row)
                    f_object.close()
                    sg.popup(values['Physiotherapist_name'] + " was added successfully", font=("Helvetica", 20, "bold"))
                    break
        window7.close()


def open_window_patient():
    layout1 = [
        [sg.Text('Pls fill out the fields:', size=(25, 2), font=("Helvetica", 20, "bold"))],
        [sg.Text("Patient_id", size=(25, 2), font=("Helvetica", 20, "bold"))],
        [sg.InputText(key='Patient_id', size=(25, 2), font=("Helvetica", 20, "bold"))],
        [sg.Text("Patient_name", size=(25, 2), font=("Helvetica", 20, "bold"))],
        [sg.InputText(key='Patient_name', size=(25, 2), font=("Helvetica", 20, "bold"))],
        [sg.Text("Est_healing_time[weeks]", size=(25, 2), font=("Helvetica", 18, "bold"))],
        [sg.InputText(key='Est_healing_time[weeks]', size=(25, 2), font=("Helvetica", 18, "bold"))],
        [sg.B('Register patient', size=(25, 3), font=("Helvetica", 20, "bold"))],
        [sg.B('Clear', size=(25, 3), font=("Helvetica", 20, "bold"))],
        [sg.B('Exit', size=(25, 3), font=("Helvetica", 20, "bold"))],
    ]

    window1 = sg.Window("Patient Window", layout1, modal=True, finalize=True)
    while True:
        event, values = window1.read()
        #        new_patient = patient(patient_id=int(values['Patient_id']), patient_name=values['Patient_name'])
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == 'Register patient':
            for i in range(len(df_of_patients)):
                if int(values['Patient_id']) == df_of_patients.loc[i, 'Patient_id']:
                    sg.popup("this id is already in use, please use a new one", font=("Helvetica", 20, "bold"))
                    break
            else:
                row = [int(values['Patient_id']), values['Patient_name'], values["Est_healing_time[weeks]"]]
                with open('patients.csv', 'a', newline='') as f_object:
                    writer_object = writer(f_object)
                    writer_object.writerow(row)
                    f_object.close()
                    sg.popup(values['Patient_name'] + " was added successfully", font=("Helvetica", 20, "bold"))
                    break
        window1.close()


def open_window_rehab_plan():
    layout2 = [
        [sg.Text('Pls fill out the fields:', size=(25, 2), font=("Helvetica", 18, "bold"))],
        [sg.Text("num_of_sets", size=(25, 2), font=("Helvetica", 18, "bold"))],
        [sg.InputText(key='num_of_sets', size=(25, 2), font=("Helvetica", 18, "bold"))],
        [sg.Text("num_of_reps", size=(25, 2), font=("Helvetica", 18, "bold"))],
        [sg.InputText(key='num_of_reps', size=(25, 2), font=("Helvetica", 18, "bold"))],
        [sg.Text("rest_between_sets[sec]", size=(25, 2), font=("Helvetica", 18, "bold"))],
        [sg.InputText(key='rest_between_sets[sec]', size=(25, 2), font=("Helvetica", 18, "bold"))],
        [sg.Text("resistance[kg]", size=(25, 2), font=("Helvetica", 18, "bold"))],
        [sg.InputText(key='resistance[kg]', size=(25, 2), font=("Helvetica", 18, "bold"))],
        [sg.B('Exit', size=(25, 3), font=("Helvetica", 18, "bold"))],
        [sg.B('Submit', size=(25, 3), font=("Helvetica", 18, "bold"))],
    ]
    window2 = sg.Window("Rehab plan Window", layout2, finalize=True)
    while True:
        event, values = window2.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Submit":
            plan_id = len(df_of_rehab_plans) + 1
            row = [plan_id, values['num_of_sets'], values["num_of_reps"],
                   values["rest_between_sets[sec]"], values["resistance[kg]"]]
            with open('rehab_plans.csv', 'a', newline='') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(row)
                f_object.close()
                sg.popup("Plan was added successfully", font=("Helvetica", 20, "bold"))
            # physiotherapist.building_rehab_plan(physiotherapist, sg.InputText(key='Plan_ID'), [1, 2, 3, 4])
    window2.close()


def first_window_physo():
    layout = [
        [sg.Text('Pls fill out the fields:', size=(25, 2), font=("Helvetica", 20, "bold"))],
        [sg.Column([[sg.Text("Physiotherapist_id", size=(25, 2), font=("Helvetica", 20, "bold"))],
                    [sg.InputText(key='Physiotherapist_id', size=(25, 2), font=("Helvetica", 20, "bold"))],
                    [sg.B("Login", size=(25, 3), font=("Helvetica", 20, "bold"))],
                    [sg.B("Exit", size=(25, 3), font=("Helvetica", 20, "bold"))]], element_justification='right'),
         sg.Image(filename='pyhsio.PNG')]
    ]
    window = sg.Window("register Window", layout, modal=True, finalize=True)
    while True:
        events, values = window.read()
        #      print(int(values["Physiotherapist_id"]))
        if events == sg.WIN_CLOSED or events == 'Exit':
            break
        if events == 'Login':
            for i in range(len(pd_of_physios)):
                if int(values['Physiotherapist_id']) == pd_of_physios.loc[i, 'Physiotherapist_id']:
                    window.close()
                    sg.popup("Hello   " + pd_of_physios.loc[i, 'Physiotherapist_name'], font=("Helvetica", 40, "bold"))
                    entry_form()
                    break
    window.close()


def first_window_patient():
    layout = [
        [sg.Text('Pls fill out the fields:', size=(25, 2), font=("Helvetica", 20, "bold"))],
        [sg.Column([[sg.Text("Patient_id", size=(25, 2), font=("Helvetica", 20, "bold"))],
                    [sg.InputText(key='Patient_id', size=(25, 2), font=("Helvetica", 20, "bold"))],
                    [sg.B("Login", size=(25, 3), font=("Helvetica", 20, "bold"))],
                    [sg.B("Exit", size=(25, 3), font=("Helvetica", 20, "bold"))]], element_justification='right'),
         sg.Image(filename='patient.PNG')]
    ]
    window = sg.Window("Patient Window", layout, modal=True, finalize=True)
    while True:
        events, values1 = window.read()
        #      print(int(values["Physiotherapist_id"]))
        if events == sg.WIN_CLOSED or events == 'Exit':
            break
        if events == 'Login':
            for i in range(len(df_of_patients)):
                if int(values1['Patient_id']) == df_of_patients.loc[i, 'Patient_id']:
                    window.close()
                    sg.popup("Hello   " + df_of_patients.loc[i, 'Patient_name'], font=("Helvetica", 40, "bold"))
                    layout0 = [
                        [sg.Text('Welcome to your window:Enjoy your stay!', size=(25, 2),
                                 font=("Helvetica", 20, "bold"))],
                        [sg.Column([[sg.B('View_graph', size=(25, 3), font=("Helvetica", 20, "bold"))],
                                    [sg.B('View_bar', size=(25, 3), font=("Helvetica", 20, "bold"))],
                                    [sg.B("Start_session", size=(25, 3), font=("Helvetica", 20, "bold"))],
                                    [sg.B("Exit", size=(25, 3), font=("Helvetica", 20, "bold"))]],
                                   element_justification='right'),
                         sg.Image(filename='prog.PNG')]
                    ]

                    assigned_plans = physiotherapist.import_csv(physiotherapist, "assigned_plans.csv")
                    rehab_plans = physiotherapist.import_csv(physiotherapist, "rehab_plans.csv")
                    reps_achieved = []
                    sessions = []
                    work_rate = rehab_plans['num_of_sets'] * rehab_plans['num_of_reps']
                    work_rate1 = []
                    window0 = sg.Window("Patient_Window", layout0, modal=True, finalize=True)
                    window0.maximize()
                    event, values = window0.read()
                    match = df_of_plans.loc[df_of_plans['Patient_id'] == int(values1['Patient_id'])].index
                    for i in match:
                        reps_achieved.append(assigned_plans.iloc[i]['total_num_of_reps_achieved'])
                        sessions.append(assigned_plans.iloc[i]['number_of_total_sessions'])
                        plan_id = assigned_plans.iloc[i]['Plan_id']
                        cnt1 = 0
                        for j in rehab_plans['Plan_id']:
                            if j == plan_id:
                                work_rate1.append(work_rate[cnt1])
                            cnt1 = cnt1 + 1
                    print(reps_achieved, work_rate1)
                    print(work_rate)
                    ratio = [x * 100 / y for x, y in zip(reps_achieved, work_rate1)]
                    print(ratio)
                    # plt.plot(list_of_max)
                    while True:
                        if event == "Exit" or event == sg.WIN_CLOSED:
                            break
                        if event == 'View_graph':
                            plt.figure(1)
                            plt.plot(sessions, ratio, label='Patient_id   ' + (values1['Patient_id']), linewidth=3)
                            plt.hlines(y=max(ratio), xmin=0, xmax=len(sessions) + 2, colors="green",
                                       linestyles='dotted')
                            plt.xlabel("Number of total sessions", fontsize=50, fontweight='bold')
                            plt.ylabel("Improvement ratio[%]", fontsize=50, fontweight='bold')
                            plt.xticks(fontsize=44)
                            plt.yticks(fontsize=44)
                            plt.subplots_adjust(left=None, bottom=0.158, right=None, top=0.925, wspace=None,
                                                hspace=None)
                            plt.show()
                            break
                        if event == 'View_bar':
                            plt.figure(2)
                            plt.bar(range(1, len(sessions) + 1), ratio, label='Patient_id   ' + (values1['Patient_id']))
                            plt.xlabel("Number of total sessions", fontsize=50, fontweight='bold')
                            plt.ylabel("Improvement ratio[%]", fontsize=50, fontweight='bold')
                            plt.xticks(fontsize=44)
                            plt.yticks(fontsize=44)
                            plt.subplots_adjust(left=None, bottom=0.158, right=None, top=0.925, wspace=None,
                                                hspace=None)
                            plt.show()
                            break
                        if event == "Start_session":
                            window0.close()
                            open_window_session()
                            break
                    window0.close()
    #     if values['Patient_id'] = "" :
    #        sg.popup("please enter a valid id ", font=("Helvetica", 40, "bold"))

    window.close()


def open_graph_window():
    layout0 = [
        [sg.Column([[sg.Text('Pls fill out the fields:', size=(25, 2), font=("Helvetica", 20, "bold"))],
                    [sg.Text("Patient_id", size=(25, 2), font=("Helvetica", 20, "bold"))],
                    [sg.InputText(key='Patient_id', size=(25, 3), font=("Helvetica", 20, "bold"))],
                    [sg.Text("Patient_id2", size=(25, 2), font=("Helvetica", 20, "bold"))],
                    [sg.InputText(key='Patient_id2', size=(25, 2), font=("Helvetica", 20, "bold"))],
                    [sg.B('View_graph', size=(25, 3), font=("Helvetica", 20, "bold"))],
                    [sg.B('Compare_patients_progress', size=(25, 2), font=("Helvetica", 20, "bold"))],
                    [sg.B('View_bar', size=(25, 3), font=("Helvetica", 20, "bold"))],
                    [sg.B('Exit', size=(25, 3), font=("Helvetica", 20, "bold"))]],
                   element_justification='right'),
         sg.Image(filename='progress.PNG')]

    ]
    assigned_plans = physiotherapist.import_csv(physiotherapist, "assigned_plans.csv")
    rehab_plans = physiotherapist.import_csv(physiotherapist, "rehab_plans.csv")
    reps_achieved = []
    sessions = []
    work_rate = rehab_plans['num_of_sets'] * rehab_plans['num_of_reps']
    work_rate1 = []
    window0 = sg.Window("Graph_Window", layout0, modal=True)
    event, values = window0.read()
    match = df_of_plans.loc[df_of_plans['Patient_id'] == int(values['Patient_id'])].index
    for i in match:
        reps_achieved.append(assigned_plans.iloc[i]['total_num_of_reps_achieved'])
        sessions.append(assigned_plans.iloc[i]['number_of_total_sessions'])
        plan_id = assigned_plans.iloc[i]['Plan_id']
        cnt1 = 0
        for j in rehab_plans['Plan_id']:
            if j == plan_id:
                work_rate1.append(work_rate[cnt1])
            cnt1 = cnt1 + 1
    print(reps_achieved, work_rate1)
    print(work_rate)
    ratio = [x * 100 / y for x, y in zip(reps_achieved, work_rate1)]
    print(ratio)
    # plt.plot(list_of_max)
    while True:
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == 'View_graph':
            plt.figure(1)
            plt.plot(sessions, ratio, label='Patient_id   ' + (values['Patient_id']), linewidth=3)
            plt.hlines(y=max(ratio), xmin=0, xmax=len(sessions) + 2, colors="green", linestyles='dotted')
            plt.xlabel("Number of total sessions", fontsize=50, fontweight='bold')
            plt.ylabel("Improvement ratio[%]", fontsize=50, fontweight='bold')
            plt.xticks(fontsize=44)
            plt.yticks(fontsize=44)
            plt.subplots_adjust(left=None, bottom=0.158, right=None, top=0.925, wspace=None,
                                hspace=None)
            plt.show()
            break
        if event == 'View_bar':
            plt.figure(2)
            plt.bar(range(1, len(sessions) + 1), ratio)
            plt.xlabel("Number of total sessions", fontsize=50, fontweight='bold')
            plt.ylabel("Improvement ratio[%]", fontsize=50, fontweight='bold')
            plt.xticks(fontsize=44)
            plt.yticks(fontsize=44)
            plt.subplots_adjust(left=None, bottom=0.158, right=None, top=0.925, wspace=None,
                                hspace=None)
            plt.show()
            break
        if event == 'Compare_patients_progress':
            reps_achieved1 = []
            sessions1 = []
            work_rate1 = rehab_plans['num_of_sets'] * rehab_plans['num_of_reps']
            work_rate2 = []
            match1 = df_of_plans.loc[df_of_plans['Patient_id'] == int(values['Patient_id2'])].index
            for i in match1:
                reps_achieved1.append(assigned_plans.iloc[i]['total_num_of_reps_achieved'])
                sessions1.append(assigned_plans.iloc[i]['number_of_total_sessions'])
                plan_id1 = assigned_plans.iloc[i]['Plan_id']
                cnt1 = 0
                for j in rehab_plans['Plan_id']:
                    if j == plan_id1:
                        work_rate2.append(work_rate1[cnt1])
                    cnt1 = cnt1 + 1
            print(reps_achieved1, work_rate2)
            print(work_rate1)
            ratio1 = [x * 100 / y for x, y in zip(reps_achieved1, work_rate2)]
            print(ratio1)
            plt.figure(3)
            plt.plot(sessions, ratio, label='Patient_id   ' + (values['Patient_id']), linewidth=3)
            plt.plot(sessions1, ratio1, label='Patient_id2  ' + (values['Patient_id2']), linewidth=3)
            plt.legend(fontsize=27,loc="upper left")
            plt.xlabel("Number of total sessions", fontsize=50, fontweight='bold')
            plt.ylabel("Improvement ratio[%]", fontsize=50, fontweight='bold')
            plt.xticks(fontsize=44)
            plt.yticks(fontsize=44)
            plt.subplots_adjust(left=None, bottom=0.158, right=None, top=0.925, wspace=None,
                                hspace=None)
            plt.show()
            break
    window0.close()


def entry_form():
    layout4 = [[sg.Column([[sg.Text('Welcome to your window', size=(20, 2), font=('Helvetica', 30, "bold"))],
                            [sg.B("Enter new patient", size=(25, 2), font=("Helvetica", 20, "bold"))],
                            [sg.B('Enter rehab plan', size=(25, 2), font=("Helvetica", 20, "bold"))],
                            [sg.B("Convert patients list  to CSV", size=(25, 2), font=("Helvetica", 20, "bold"))],
                            [sg.B("Enter new physiotherapist", size=(25, 2), font=("Helvetica", 20, "bold"))],
                            [sg.B("Assign plan to patient", size=(25, 2), font=("Helvetica", 20, "bold"))],
                            [sg.B("View patient progress", size=(25, 2), font=("Helvetica", 20, "bold"))],
                            [sg.B("Exit", size=(25, 2), font=("Helvetica", 20, "bold"))]],
                           element_justification = 'right'),
    sg.Image(filename='pyhsiotera.PNG', size=(2500, 2000))]
    ]

    window4 = sg.Window("data entry form", layout4, finalize=True)
    window4.maximize()
    while True:
        event, values = window4.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Enter new patient":
            open_window_patient()
        if event == 'Enter new physiotherapist':
            register_window_physio()
        if event == "Enter rehab plan":
            open_window_rehab_plan()
        if event == 'Convert patients list  to CSV':
            df_of_patients.to_csv(r'C:\Users\USER\PycharmProjects\pythonProject\updated_patients.csv',
                                  index=False)
            sg.popup('file has been converted successfully', font=("Helvetica", 20, "bold"))
        if event == "View patient progress":
            open_graph_window()
        if event == "Assign plan to patient":
            layout6 = [
                [sg.Column([[sg.Text('pls fill out the fields:', size=(25, 2), font=("Helvetica", 20, "bold"))],
                            [sg.Text('Plan_id', size=(25, 2), font=("Helvetica", 20, "bold"))],
                            [sg.InputText(key='Plan_id', size=(25, 2), font=("Helvetica", 20, "bold"))],
                            [sg.Text("Patient_id", size=(25, 2), font=("Helvetica", 20, "bold"))],
                            [sg.InputText(key='Patient_id', size=(25, 2), font=("Helvetica", 20, "bold"))],
                            [sg.B("Submit", size=(25, 3), font=("Helvetica", 20, "bold"))],
                            [sg.B("Exit", size=(25, 3), font=("Helvetica", 20, "bold"))]],
                           element_justification='right'),
                 sg.Image(filename='pyhsiosys.PNG')]
            ]
            window6 = sg.Window("Assign plan form", layout6)
            while True:
                event, values = window6.read()
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                if event == "Submit":
                    session_id = len(df_of_plans) + 1
                    match = df_of_rehab_plans.index[df_of_rehab_plans['Plan_id'] == int(values['Plan_id'])].tolist()
                    matchs = match[0]
                    if int(values["Patient_id"]) in list(df_of_plans.loc[:, 'Patient_id']):
                        num_total_sessions = df_of_plans['Patient_id'].value_counts()[int(values['Patient_id'])] + 1
                    else:
                        num_total_sessions = 1
                    if int(values["Patient_id"]) in df_of_patients.loc[:, 'Patient_id'] and int(
                            cnt_success_reps) <= df_of_rehab_plans.loc[matchs, 'num_of_sets'] * \
                            df_of_rehab_plans.loc[matchs, 'num_of_reps']:
                        if int(values["Plan_id"]) in df_of_plans.loc[:, 'Plan_id']:
                            row = [session_id, values['Plan_id'], values["Patient_id"],
                                   cnt_success_reps, num_total_sessions]
                            with open('assigned_plans.csv', 'a', newline='') as f_object:
                                writer_object = writer(f_object)
                                writer_object.writerow(row)
                                f_object.close()
                                sg.popup("Session was added successfully", font=("Helvetica", 20, "bold"))
                                window6.close()
                        else:
                            sg.popup('this plan id isnt valid ', font=("Helvetica", 20, "bold"))
                    else:
                        sg.popup('this patient id isnt valid or number of reps is greater then the max for this plan ',
                                 font=("Helvetica", 20, "bold"))
    window4.close()


layout5 = [
    [sg.Text('welcome to our rehabilitation system', justification='center', size=(40, 3),
             font=('Helvetica', 40, "bold"))],
    [sg.Image(filename='rehab.PNG')],
    [sg.B('Patient', size=(20, 3), font=("Helvetica", 30, "bold")),
     sg.B('Physiotherapist', size=(20, 3), font=("Helvetica", 30, "bold")),
     sg.B('Exit', size=(20, 3), font=("Helvetica", 30, "bold"))],

]
window5 = sg.Window("GUI_Window", layout5, finalize=True)

# Load and draw the image on the canvas

window5.maximize()

while True:
    event, values = window5.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == 'Physiotherapist':
        first_window_physo()
    if event == 'Patient':
        first_window_patient()
window5.close()
