from rehab_plan import rehab_plan     # First is the file, second is the class
import exercise
from patient import patient
import pandas as pd
import csv
import matplotlib.pyplot as plt


class physiotherapist(object):



###  -----------------------------------------------Contructor - ----------------------------------------------------###

    def __init__(self, physiotherapist_id, physiotherapist_name):
        self.physiotherapist_id = physiotherapist_id
        self.physiotherapist_name = physiotherapist_name
        self.physio_plans = {}  # Dict {key - plan_id, value - list_of_workouts}
        self.patients = []  # Dict {key - patient_id, value -patient }

    ###-----------------------------------------------Manage plans------------------------------------------------###

    def building_rehab_plan(self, plan_id, list_of_Exercises_id):
        self.physio_plans.update({plan_id: list_of_Exercises_id})


    def append_new_workout(self, plan_id, new_workout):

        self.physio_plans[plan_id] += ", " + new_workout

    # def choose_ideal_plan(self, healing_time):
    #  if healing_time >= rehab_plan.:
    #     print("the ideal plans are{}".format(rehab_plan.plan_id))

    def delete_workout(self, plan_id):

        self.physio_plans[plan_id] = ()

    def get_last_workout_id(self):
        last_workout_list = list(self.physio_plans.keys())[-1]
        print(last_workout_list)

    ###-----------------------------------------------Manage plans------------------------------------------------###


    def create_new_physio(self, physiotherapist_id, physiotherapist_name):

        return physiotherapist(physiotherapist_id, physiotherapist_name)


    def __eq__(self, other):
        if self.physiotherapist_id == other.physiotherapist_id:
            return True
        else:
            return False
#todo -new
#השלמתי את כל הפונקציה והוסםתי מלל
    def assign_patients_to_physio(self):

        add_next_patient = True

        while(add_next_patient):

            patient_id = int(input("enter_patient_id   "))
            name = str(input("patient_name   "))
            new_patient = patient(patient_id=patient_id, patient_name=name, address=None)
            self.patients.append({'patient_id': patient_id, 'patient_name': name})
            name1 = int(input("to stop enter 0, to enter another patient enter 1   "))
            if name1 == 0:
                add_next_patient = False
#todo -new
    #def physio_sees_patients(self):
     #    for k, v in self.patients.items():
      #      print(k, v)




    def __str__(self):

         return f"{self.physiotherapist_id} is this pysio id , and {self.physiotherapist_name} is its name"


  #todo -new
    def import_csv(self,file_name):

        df = pd.read_csv(file_name)
        return df
    def create_csv_of_patients(self):
        features = ['patient_id', 'patient_name']
        with open('patients.csv', 'w') as file:
           writer = csv.DictWriter(file, fieldnames=features)
           writer.writeheader()
           writer.writerows(self.patients)



###-----------------------------------------------main------------------------------------------###

new_ph = physiotherapist(1, 'moe')
p2 = physiotherapist(2, 'moshe')
list_of_new_workouts = '5*' + exercise.Ex1.exercise_name
new_ph.building_rehab_plan(1, list_of_new_workouts)
print(new_ph.physio_plans)
new_ph.building_rehab_plan(2, list_of_new_workouts)

print(new_ph.physio_plans)
new_ph.get_last_workout_id()
print(new_ph)
print(new_ph == p2)
a = physiotherapist.create_new_physio(physiotherapist, 3, "yoav")
print(a)
#a.assign_patients_to_physio()
work_rate= a.import_csv("rehab_plans.csv")
est_error=a.import_csv("est_error.csv")
print(work_rate, est_error)
#a.physio_sees_patients()
#a.create_csv_of_patients()
