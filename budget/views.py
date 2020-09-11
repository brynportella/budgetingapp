from django.shortcuts import render

from accounts.models import AccountType, Account, AccountEntry
from .models import (AnticipatedTransaction, ExpenseType, BudgetExpense,
                     Income, IncomeToAccount, BudgetExpenseToAccount)

# Create your views here.
def budgetpage(request):
  context = {}
  if request.user.is_authenticated:
    user = request.user
    print("OK")
    # Bank statement
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
    

