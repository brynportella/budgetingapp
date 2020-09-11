from django.shortcuts import render

# Create your views here.
def goalspage(request):
  context = {}
  return render(request, 'goals.html', context)
