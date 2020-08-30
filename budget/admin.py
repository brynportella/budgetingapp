from django.contrib import admin

# Register your models here.
from .models import ExpenseType, BudgetExpense, Income, IncomeToAccount, BudgetExpenseToAccount

admin.site.register(ExpenseType)
admin.site.register(BudgetExpense)
admin.site.register(Income)
admin.site.register(IncomeToAccount)
admin.site.register(BudgetExpenseToAccount)