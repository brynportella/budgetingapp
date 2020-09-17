# accounts/views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView

from .models import Account


class AccountCreate(CreateView):
    template_name = 'new-account.html'
    model = Account
    fields = [ 'account_name', 'account_balance', 'interest_rate', 'compound_periods_per_year', 'account_details', 'account_type' ]
    success_url = 'budget'
    def form_valid(self, form):
      obj = form.save(commit=False)
      obj.user = self.request.user
      obj.save()
      return redirect('budget')

