# users/forms.py
from django import forms
# TODO: Need to figure out models to import
# from .models import CustomUser

class SavingGoalForm(forms.Form):
  goal_name = forms.CharField(label='Goal name', max_length=100)
  goal_amount = forms.DecimalField(label='Goal amount', min_value=0.0)


class SavingAccountForm(forms.Form):
  bank_name = forms.CharField(label='Bank name', max_length=100)



