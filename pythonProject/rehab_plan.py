class rehab_plan(object):

    ###-----------------------------------------------Contructor-----------------------------------------------------###

    def __init__(self, plan_id, plan_name, est_healing_time):
        self.plan_id = plan_id
        self.plan_name = plan_name
        self.est_healing_time = est_healing_time                   #[Hr]

    def __eq__(self, other):
        if type(other) is type(rehab_plan):
            return self.plan_id == other.plan_id
        return False



    def __str__(self):

         return f"{self.plan_id} is this plan id , and {self.plan_name} is its name"






###-----------------------------------------------main------------------------------------------###
plan1 = rehab_plan(1, 'push', 96)
plan2 = rehab_plan(2, 'pull', 192)

