layout6 = [
    [sg.Column([[sg.Text('pls fill out the fields:', size=(25, 2), font=("Helvetica", 20, "bold"))],
                [sg.Text('Plan_id', size=(25, 2), font=("Helvetica", 20, "bold"))],
                [sg.InputText(key='Plan_id', size=(25, 2), font=("Helvetica", 20, "bold"))],
                [sg.Text("Patient_id", size=(25, 2), font=("Helvetica", 20, "bold"))],
                [sg.InputText(key='Patient_id', size=(25, 2), font=("Helvetica", 20, "bold"))],
                [sg.Text("total_num_of_reps_achieved", size=(25, 2), font=("Helvetica", 20, "bold"))],
                [sg.InputText(key='total_num_of_reps_achieved', size=(25, 2),
                              font=("Helvetica", 20, "bold"))],
                [sg.B("Submit", size=(25, 3), font=("Helvetica", 20, "bold"))],
                [sg.B("Exit", size=(25, 3), font=("Helvetica", 20, "bold"))]],
               element_justification='right'),
     sg.Image(filename='pyhsiosys.PNG')]
]