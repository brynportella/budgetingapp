# accounts/views.py
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView

from .forms import OnboardingForm, choices
from accounts.models import AccountType, Account, AccountEntry
from budget.models import (AnticipatedTransaction, ExpenseType, BudgetExpense,
                           Income, IncomeToAccount, BudgetExpenseToAccount)
# from goals.model import # TODO Need goals

"""
commented out html:
<div class="container-fluid">
	<div class="card">
		<div class="card-body">
			<div class="card-title">
				Hi {{ user.username }}!
			</div>
			<div class="card-text">
				<a href="{% url 'logout' %}">logout</a>
			</div>
		</div>
	</div>
</div>

"""
def home(request):
  is_pay_day = True
  got_goals = True
  got_bill = True
  context = {
    'is_pay_day' : is_pay_day,
    'got_goals' : got_goals,
    'got_bill' : got_bill,
  }
  return render(request, 'home.html', context)

def onboarding(request):
  # if this is a POST request we need to process the form data
  if request.method == 'POST':
    # create a form instance and populate it with data from the request:
    form = OnboardingForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
      # process the data in form.cleaned_data as required
      # Set up bank account
      # More personal stuff
      # Store up saving goal
      # Store up self assessment
      example_cleaned_data= """{
            'bank_name': 'Bank name',
            'bank_account_name': 'Bank account name',
            'bank_account_number': 12345,
            'saving_goal_name': 'Saving goal',
            'saving_goal_amount': Decimal('100'),
            'spending': 'spending3',
            'income_question_pay_period': Decimal('1500'),
            'income_question_vary': False,
            'income_question_pay_freq': Decimal('3'),
            'bill_pay': 'billpay4',
            'bill_rent': Decimal('500'),
            'bill_utilities': Decimal('200'),
            'bill_food': Decimal('300'),
            'bill_health': Decimal('100'),
            'bill_other': Decimal('400'),
            'savings_coverage': 'savingscoverage3',
            'confidence': 'fincon3',
            'debt': 'debt4',
            'credit_score': 'creditscore4',
            'insurance': 'insurance4',
            'ethnicity': ['ethnicity2', 'ethnicity3'],
            'veteran': False
      }"""
      # redirect to a new URL:
      return HttpResponseRedirect('home.html')
  else:
    form = OnboardingForm()
  return render(request, 'onboarding.html', {'form': form})




