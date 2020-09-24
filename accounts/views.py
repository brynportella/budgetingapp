# accounts/views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView

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

class AccountUpdate(UpdateView):
  model = Account
  template_name= 'account-update.html' 
  success_url = 'accounts'
  fields = ['account_name', 'account_balance', 'interest_rate', 'compound_periods_per_year', 'account_details', 'account_type' ]
  def form_valid(self, form):
    form.save()
    return redirect('accounts')

def accounts_page(request):
  if request.user.is_authenticated:
    user = request.user
    user_accounts = Account.objects.filter(user=user)
    context = {
      'user_accounts' : user_accounts
    }
  return render(request, 'accounts.html', context)
