from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import NewGoalForm

# Create your views here.
def goalspage(request):
  context = {}
  return render(request, 'goals.html', context)

# TODO: Did not know about CreateView when I made this -- refer to AccountCreate or IncomeCreate to redo this -- SORRY (Stephen)
def newgoal(request):
  # if this is a POST request we need to process the form data
  if request.method == 'POST':
    # create a form instance and populate it with data from the request:
    form = NewGoalForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
      # process the data in form.cleaned_data as required
      # redirect to a new URL:
      return HttpResponseRedirect('home.html')
  else:
    form = NewGoalForm()
  return render(request, 'new-goals.html', {'form': form})
