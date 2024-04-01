class exercise (object):

    ###-----------------------------------------------Contructor-----------------------------------------------------###
    def __init__(self, exercise_id, exercise_name):
        self.exercise_id = exercise_id
        self.exercise_name = exercise_name


 ###-----------------------------------------------Manage Exercises------------------------------------------------###

Ex1 = exercise(1, "arm ext")
Ex2 = exercise(2, "arm flex")
Ex3 = exercise(3, "hand flex")
Ex4 = exercise(4, "hand ext")
Ex5 = exercise(5, "lat pull")
Ex6 = exercise(6, "row")


def __str__(self):
    return f"{self.exercise_id} is this ex id , and {self.exercise_name} is its name"