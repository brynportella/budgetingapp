from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
# from django.views.generic.edit import FormView
from datetime import timedelta


from accounts.models import AccountType, Account, AccountEntry
from .models import (AnticipatedTransaction, ExpenseType, BudgetExpense,
                     Income, IncomeToAccount, BudgetExpenseToAccount)


class IncomeCreate(CreateView):
    template_name = 'new-income.html'
    model = Income
    fields = ['start_date', 'recurrence_freq', 'amount', 'income_name', 'certainty']
    success_url = 'budget'
    def form_valid(self, form):
      obj = form.save(commit=False)
      obj.user = self.request.user
      obj.end_date = obj.start_date + timedelta(days=365*1000)
      obj.save()
      return redirect('budget')

class BudgetExpenseCreate(CreateView):
    template_name = 'new-budget-expense.html'
    model = BudgetExpense
    fields = ['start_date', 'recurrence_freq', 'amount', 'expense_name', 'expense_type', 'importance']
    success_url = 'budget'
    def form_valid(self, form):
      obj = form.save(commit=False)
      obj.user = self.request.user
      obj.end_date = obj.start_date + timedelta(days=365*1000)
      obj.save()
      return redirect('budget')

class BudgetExpenseUpdate(UpdateView):
  model = BudgetExpense
  template_name = 'budget-expense-update.html'
  success_url='budget'
  fields = ['start_date', 'recurrence_freq', 'amount', 'expense_name', 'expense_type', 'importance', 'end_date']
  def form_valid(self, form):
    form.save()
    return redirect('budget')

class IncomeUpdate(UpdateView):
  model = Income
  template_name= 'income-update.html' 
  success_url = 'budget'
  fields = ['start_date', 'end_date','recurrence_freq', 'amount', 'income_name', 'certainty']
  def form_valid(self, form):
    form.save()
    return redirect('budget')
    
# Create your views here.
def budgetpage(request):
  context = {}
  if request.user.is_authenticated:
    user = request.user
    # Bank statement
    # TODO How to order these?
    user_accounts = Account.objects.filter(user=user)
    user_budget = BudgetExpense.objects.filter(user=user)
    user_incomes = Income.objects.filter(user=user).order_by('start_date')

    user_acct_incomes = IncomeToAccount.objects.filter(account__in=user_accounts)
    user_acct_expenses = BudgetExpenseToAccount.objects.filter(account__in=user_accounts)
    user_acct_entry = AccountEntry.objects.filter(account__in=user_accounts)
    user_acct_expenses = BudgetExpenseToAccount.objects.filter(account__in=user_accounts)
    transactions = []
    totals = []
    # context['transactions'] = transactions
    context = {
      'user_accounts' : user_accounts,
      'user_budget' : user_budget,
      'user_incomes' : user_incomes,
    }
  return render(request, 'budget.html', context)
    

