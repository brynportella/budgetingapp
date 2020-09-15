from django.db import models
from users.models import CustomUser
from django.utils import timezone
from accounts.models import Account
from datetime import datetime

class AnticipatedTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    start_date = models.DateTimeField(default = timezone.now)
    end_date = models.DateTimeField() 
    amount = models.DecimalField(max_digits=30, decimal_places=2, null=False)
    class RecurrenceFreq(models.IntegerChoices):
        WEEKLY = 1
        BIWEEKLY = 2 # Meaning every other week
        MONTHLY = 3
        # Every 15 or so days with an interval accounting for the varying end of the month
        # i.e. the 
        TWICE_A_MONTH = 4 
        ONCE = 0
        ANNUALLY = 5
    recurrence_freq = models.IntegerField(choices = RecurrenceFreq.choices)
    bussiness_days_only = models.BooleanField(default = False)
    class Meta:
        abstract = True

class ExpenseType(models.Model):
    expense_type_name = models.CharField(max_length=100)
    def __str__(self):
        return self.expense_type_name

class BudgetExpense(AnticipatedTransaction):
    expense_name = models.CharField(max_length=150)
    class Importance(models.IntegerChoices):
        NECESSITY = 1 # Most important expenses
        BASIC_COMFORT = 2 # Create a baseline quality of life
        EXTRAVAGANCE = 3 # A splurge
    importance = models.IntegerField(choices = Importance.choices)
    expense_type = models.ForeignKey(ExpenseType, on_delete = models.SET_NULL, null=True)
    def __str__(self):
        return "{} {}: ${:.2f} | Between {} and {}\n".format(
                                AnticipatedTransaction.RecurrenceFreq(self.recurrence_freq).label, 
                                self.expense_name, 
                                self.amount, 
                                self.start_date.strftime('%B %d, %Y'),
                                self.end_date.strftime('%B %d, %Y'))

class Income(AnticipatedTransaction):
    income_name =  models.CharField(max_length=100)
    class Certainty(models.IntegerChoices):
        CERTAIN = 1 # Essentially guaranteed
        ESTIMATED = 2 # Anticipated, but the amount may vary from expected
        PROBABLE = 3 # Likely to be the case, but not guaranteed
    certainty = models.IntegerField(choices = Certainty.choices )
    def __str__(self):
        return "Income: ${:.2f} {}".format(self.amount, self.income_name)

class IncomeToAccount(models.Model):
    amount = models.DecimalField(max_digits=30, decimal_places=2, null=False)
    account = models.ForeignKey(Account, on_delete = models.CASCADE)
    income = models.ForeignKey(Income, on_delete = models.CASCADE)
    def __str__(self):
       return "Income to account: ${:.2f} {} to account [{}]".format(self.amount, self.income, self.account)

class BudgetExpenseToAccount(models.Model):
    amount = models.DecimalField(max_digits=30, decimal_places=2, null=False)
    account = models.ForeignKey(Account, on_delete = models.CASCADE)
    budget_expense = models.ForeignKey(BudgetExpense, on_delete = models.CASCADE)
    def __str__(self):
       return "Income to account: ${:.2f} from [{}] to account [{}]".format(self.amount, self.budget_expense, self.account)

