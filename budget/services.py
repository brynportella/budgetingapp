from .models import ExpenseType
from .models import BudgetExpense
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
from calendar import monthrange

def get_all_upcoming_budget_expenses():
    return BudgetExpense.objects.filter(end_date__gte = timezone.now())

#def get_all_budget_expense_occurences_in_time_frame(start_date, end_date):
#   expenses = BudgetExpense.objects()
#   for element in 

def get_budget_expense_occurences(expense, start_date, end_date):
    start_date = start_date if start_date < expense.start_date else expense.start_date
    end_date = end_date if end_date < expense.end_date else expense.end_date
    recurrence_freq = expense.recurrence_freq
    interval = -1
    # Weekly 
    if recurrence_freq == 1:
        interval = timedelta(days = 7)
    # Every other week 
    elif(recurrence_freq == 2):
        interval = timedelta(days = 14)
    occurrences = [] 
    current_occurence = start_date
    while(current_occurence <= end_date):
        occurrences.append(current_occurence)
        print("Added "+current_occurence.__str__())
        if recurrence_freq == 1 or recurrence_freq == 2:
            current_occurence += interval
            print("Now current_occurrence is "+ current_occurence.__str__())
        # Monthly
        elif recurrence_freq == 3:
            print("Monthly")
            if is_last_day_of_month(current_occurence):
                current_occurence = get_last_day_of_next_month(current_occurence)
            else: 
                current_occurence += timedelta(days = monthrange(current_occurence.year, current_occurence.month)[1])
        # Twice a month
        elif recurrence_freq == 4:
            print("Twice a month")
            if current_occurence.day == 1:
                current_occurence += timedelta(days = 14)
            else:
                current_occurence = get_last_day_of_month(current_occurence)+timedelta(days=1)
        else:
            print("Once")
            break
    expense_occurrences = {expense : occurrences}
    return expense_occurrences

def get_last_day_of_month(date):
    return date.replace(day = monthrange(date.year, date.month)[1])

def is_last_day_of_month(date):
    return date.day == get_last_day_of_month(date)

def get_last_day_of_next_month(date):
    date = get_last_day_of_month(date)
    date += date + timedelta(days=1)
    return get_last_day_of_month(date)