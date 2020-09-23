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
from budget import services
# from goals.model import # TODO Need goals

from goals.models import Goal
import datetime
from datetime import timedelta


def test(request):
  context = {}
  return render(request, 'test.html', context)

def test2(request):
  context = {}
  return render(request, 'test2.html', context)


def home(request):
  user = request.user
  if not user.is_authenticated:
    return render(request, 'home.html')
   # Goals
  goals = Goal.objects.filter(user=user).order_by('start_date')[:3]
  # Pop-ups
  is_pay_day = services.is_pay_day(user = user)
  got_goals = len(goals) > 0
  got_bill = services.has_bills(user=user, start_date=timezone.now(), end_date= timezone.now()+timedelta(days=30))
  # Recommendations logic
  recommendations_text = [
    'Recommendation placeholder text 1',
    'Recommendation placeholder text 2',
    'Recommendation placeholder text 3',
  ]
  goal_percentage_completion = []
  for goal in goals:
    current_goal_percentage = (goal.progress / goal.amount)*100
    goal_percentage_completion.append(current_goal_percentage)

  # Get cash
  user_accounts = Account.objects.filter(user=user)
  cash = sum([ x.account_balance for x in user_accounts ])
  user_budget = BudgetExpense.objects.filter(user=user)
  bills = services.calculate_total_user_expense_value_in_timeperiod(user, timezone.now(), timezone.now()+timedelta(days=30))
  # Build contex
  context = {
    'is_pay_day' : is_pay_day,
    'got_goals' : got_goals,
    'got_bill' : got_bill,
    'recommendations_text': recommendations_text,
    'goals': goals,
    'cash' : cash,
    'bills' : bills,
    'goals_percentage_completion': goal_percentage_completion,
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




