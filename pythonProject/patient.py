import exercise
class patient(object):

    ###-----------------------------------------------Contructor-----------------------------------------------------###

    def __init__(self,patient_id, patient_name):

        self.patient_id = patient_id
        self.patient_name = patient_name
        self.rehab_plan = {}  # Dict {key - update, value - list_of_workouts}
        self.number_of_updates = 1



    ###-----------------------------------------------Manage Workouts------------------------------------------------###

    def create_new_patient(self, patient_id, patient_name):

        return patient(patient_id = patient_id, patient_name = patient_name)



    def view_my_last_workout(self):

        last_workout_list = self.rehab_plan.get(self.number_of_updates)

        for i in last_workout_list:

            print(i)




#p-2
    def patient_views_progress(self,view_my_last_workout):

        view_my_last_workout = self.rehab_plan.get(self.last_workout_list)



###-----------------------------------------------Compare and String Methods------------------------------------------###
    # todo -new
    def __eq__(self, other):
        if self.patient_id == other.patient_id:
            return True
        else:
            return False
    def __str__(self):
        return f"{self.patient_id} is this patient id , and {self.patient_name} is its name"




###-----------------------------------------------main------------------------------------------###

new_p=patient.create_new_patient(patient,1,'omer')
print(new_p)




