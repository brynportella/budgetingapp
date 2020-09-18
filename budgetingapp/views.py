# accounts/views.py
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils import timezone

from .forms import OnboardingForm, choices
from accounts.models import AccountType, Account, AccountEntry
from budget.models import (AnticipatedTransaction, ExpenseType, BudgetExpense,
                           Income, IncomeToAccount, BudgetExpenseToAccount)
# from goals.model import # TODO Need goals

import datetime

######################################################################
##### DEBUG #####
######################################################################
##### WE WILL REPLACE THIS WITH GOALS MODEL #####
##### I DO NOT KNOW IF THESE FIELDS WILL BE USED #####
class TempGoal:
  def __init__(self, id_num, name, value, goal):
    self.id = id_num
    self.name = name
    self.value = value
    self.goal = goal
    self.percentage = int(100*value / goal)

def test(request):
  context = {}
  return render(request, 'test.html', context)

def test2(request):
  context = {}
  return render(request, 'test2.html', context)

# TODO: This should probably be tied to the class itself...
RecurrenceFreqString = {
  AnticipatedTransaction.RecurrenceFreq.ONCE : "once",
  AnticipatedTransaction.RecurrenceFreq.WEEKLY : "weekly",
  AnticipatedTransaction.RecurrenceFreq.BIWEEKLY : "biweekly",
  AnticipatedTransaction.RecurrenceFreq.MONTHLY : "monthly",
  AnticipatedTransaction.RecurrenceFreq.TWICE_A_MONTH : "twice a month",
}

# TODO: This should also probably be tied to class
RecurrenceFreqToNumTimesPerMonth = {
  AnticipatedTransaction.RecurrenceFreq.ONCE : 1,
  AnticipatedTransaction.RecurrenceFreq.WEEKLY : 4,
  AnticipatedTransaction.RecurrenceFreq.BIWEEKLY : 2,
  AnticipatedTransaction.RecurrenceFreq.MONTHLY : 1,
  AnticipatedTransaction.RecurrenceFreq.TWICE_A_MONTH : 2,
}

# TODO: We should make this flexible to handle any time period
def budgets_to_monthly(budgets):
  now = timezone.now() # TODO: Need to make this the client timezone
  s = 0
  for budget in budgets:
    # TODO: This logic is not all technically correct
    if budget.start_date <= now <= budget.end_date:
      s += RecurrenceFreqToNumTimesPerMonth[budget.recurrence_freq]*budget.amount
  return s


######################################################################
##### END DEBUG #####
######################################################################



def home(request):
  user = request.user
  if not user.is_authenticated:
    return render(request, 'home.html')
  # DEBUG: All placeholders
  # Pop-ups
  is_pay_day = False
  got_goals = True
  got_bill = False
  # Recommendations logic
  recommendations_text = [
    'Recommendation placeholder text 1',
    'Recommendation placeholder text 2',
    'Recommendation placeholder text 3',
  ]
  # Goals
  goals = [
    TempGoal(1,'Save 100 Dollars', 25, 100),
    TempGoal(2,'Pay Debt', 0.9*2000, 2000),
    TempGoal(3,'Nice dinner out', 0.35*80, 80),
  ]
  # Get cash
  user_accounts = Account.objects.filter(user=user)
  cash = sum([ x.account_balance for x in user_accounts ])
  user_budget = BudgetExpense.objects.filter(user=user)
  bills = budgets_to_monthly([ x for x in user_budget ])
  # Build contex
  context = {
    'is_pay_day' : is_pay_day,
    'got_goals' : got_goals,
    'got_bill' : got_bill,
    'recommendations_text': recommendations_text,
    'goals': goals,
    'cash' : cash,
    'bills' : bills,
  }
  print(request)
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




