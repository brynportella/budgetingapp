# accounts/views.py
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import OnboardingForm


#############################################################################
############################ Temporary Templates ############################
#############################################################################

def onboarding(request):
  # if this is a POST request we need to process the form data
  if request.method == 'POST':
    # create a form instance and populate it with data from the request:
    form = OnboardingForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
      # process the data in form.cleaned_data as required
      # TODO: What to do here?
      print(form.cleaned_data)
      # redirect to a new URL:
      return HttpResponseRedirect('home.html')
    else:
      print("FORM NOT VALID")
  else:
    form = OnboardingForm()
  return render(request, 'onboarding.html', {'form': form})

def saving_goal(request):
  # if this is a POST request we need to process the form data
  if request.method == 'POST':
    # create a form instance and populate it with data from the request:
    form = SavingGoalForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
      # process the data in form.cleaned_data as required
      # TODO: What to do here?
      # redirect to a new URL:
      return HttpResponseRedirect('link-savings')

  # if a GET (or any other method) we'll create a blank form
  else:
    form = SavingGoalForm()

  return render(request, 'onboarding/saving-goal.html', {'form': form,
                                                         'next': 'link-savings'})

def link_savings(request):
  return render(request, 'onboarding/link-savings.html', {'prev': 'saving-goal',
                                                          'next':'spending-vs-income'})


def spending_vs_income(request):
  return render(request, 'onboarding/spending-vs-income.html', {'prev': 'link-savings'})




