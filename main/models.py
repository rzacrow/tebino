from django.db import models
import pandas as ps

class State(models.Model):
    def STATE_CHOICES() -> str:
        states = ps.read_excel(io='states.xlsx', sheet_name='DB')
        iran = list()
        states_list = list()
        for state in states['State']:
            if state not in states_list:
                states_list.append(state)
        
        for state in states_list:
            iran.append((1,state))
        return iran

    name = models.CharField(choices=STATE_CHOICES, max_length=256, unique=True, blank=False, null=False)

class City(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)