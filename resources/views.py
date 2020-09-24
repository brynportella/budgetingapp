from django.shortcuts import render
from .models import Resource
from django.views.generic.list import ListView

class ResourceListView(ListView): 
    model = Resource


