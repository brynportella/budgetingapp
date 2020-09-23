from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponseRedirect
from .forms import NewGoalForm
from .models import Goal
import django.utils.timezone as timezone

class GoalCreate(CreateView):
    template_name = 'new-goals.html'
    model = Goal
    fields = [ 'goal_type', 'goal_reason', 'amount', 'end_date' ]
    success_url = 'home.html'
    def form_valid(self, form):
      obj = form.save(commit=False)
      obj.user = self.request.user
      obj.start_date = timezone.now()
      obj.progress = 0.0
      obj.save()
      return redirect('home.html')

class GoalUpdate(UpdateView):
    template_name = 'goals.html'
    model = Goal
    fields = [ 'goal_type', 'goal_reason', 'amount', 'progress', 'start_date', 'end_date' ]
    success_url = '/home.html'

# #  Did not know about CreateView when I made this -- refer to AccountCreate or IncomeCreate to redo this -- SORRY (Stephen)
# def newgoal(request):
#   # if this is a POST request we need to process the form data
#   if request.method == 'POST':
#     # create a form instance and populate it with data from the request:
#     form = NewGoalForm(request.POST)
#     # check whether it's valid:
#     if form.is_valid():
#       # process the data in form.cleaned_data as required
#       # redirect to a new URL:
#       return HttpResponseRedirect('home.html')
#   else:
#     form = NewGoalForm()
#   return render(request, 'new-goals.html', {'form': form})
