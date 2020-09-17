from django import forms
from django.forms import DateTimeInput

from .models import GoalType

# TODO: Move this to a utils folder?
class NewGoalForm(forms.Form):
  # Tab 1: Goal name
  goal_name = forms.CharField(label='What do you want to name it?', max_length=100)
  # Tab 2: Goal amount
  goal_amount = forms.DecimalField(label='What amount do you need to save for this?', min_value=0.0)
  # Tab 3: Goal target date
  goal_date = forms.DateTimeField(label='When do you want to have that done by?', input_formats=['%d/%m/%Y %H:%M'])
  # Tab 3: Goal reason
  goal_reason = forms.CharField(label='Why do you want to achieve this goal?', max_length=100)


