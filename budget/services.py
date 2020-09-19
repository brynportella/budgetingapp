from .models import ExpenseType
from .models import BudgetExpense, Income
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
from calendar import monthrange, weekday
import holidays

def get_all_upcoming_budget_expenses(user):
    return BudgetExpense.objects.filter(user = user, end_date__gte = timezone.now())

def get_all_upcoming_anticipated_income(user):
    return Income.objects.filter(user = user).filter(end_date__gte = timezone.now())

def get_anticipated_transaction_occurences(anticipated_transaction, start_date, end_date):
    end_date = end_date if end_date < anticipated_transaction.end_date else anticipated_transaction.end_date
    recurrence_freq = anticipated_transaction.recurrence_freq
    interval = get_freq_based_interval(recurrence_freq)
    is_business_days_only = anticipated_transaction.bussiness_days_only
    occurrences = [] 
    current_occurence = anticipated_transaction.start_date
    bussiness_day_occurence =  get_closest_business_day(anticipated_transaction.start_date)
    while(less_than_or_equal_to_time_insensitive(current_occurence, end_date) or 
                (is_business_days_only and less_than_or_equal_to_time_insensitive(bussiness_day_occurence, end_date))):
        if(greater_than_or_equal_to_time_insensitive(current_occurence, start_date) and (not is_business_days_only)):
            occurrences.append(current_occurence)
        elif greater_than_or_equal_to_time_insensitive(bussiness_day_occurence, start_date):
            occurrences.append(bussiness_day_occurence)
        # Weekly and Biweekly
        if recurrence_freq == 1 or recurrence_freq == 2:
            current_occurence += interval
        # Monthly
        elif recurrence_freq == 3:
            if is_last_day_of_month(current_occurence):
                current_occurence = get_last_day_of_next_month(current_occurence)
            else: 
                current_occurence += timedelta(days = monthrange(current_occurence.year, current_occurence.month)[1])
        # Twice a month
        elif recurrence_freq == 4:
            if current_occurence.day <= 14:
                current_occurence += timedelta(days = 14)
            else:
                number_of_days = current_occurence.day - 14
                current_occurence = get_last_day_of_month(current_occurence)+timedelta(days=number_of_days)
        elif recurrence_freq == 5:
            current_occurence = current_occurence.replace(year = current_occurence.year + 1) 
        else:
            break
        bussiness_day_occurence = get_closest_business_day(current_occurence)

    expense_occurrences = {anticipated_transaction : occurrences}
    return expense_occurrences

def get_last_day_of_month(date):
    return date.replace(day = monthrange(date.year, date.month)[1])

def is_last_day_of_month(date):
    return date.day == get_last_day_of_month(date)

def get_last_day_of_next_month(date):
    date = get_last_day_of_month(date)
    date += date + timedelta(days=1)
    return get_last_day_of_month(date)

def get_freq_based_interval(recurrence_freq):
    interval = -1 
    if recurrence_freq == 1: 
        interval = timedelta(days = 7)
    elif recurrence_freq == 2: 
        interval = timedelta(days = 14)
    return interval

def get_all_occurences_of_all_expenses_for_dates(user, begin_date, finish_date):
    budget_expenses = BudgetExpense.objects.filter(user=user, end_date__gte = begin_date)
    matching_budget_expenses = {}
    for budget_expense in budget_expenses:
        current_occurrences = get_anticipated_transaction_occurences(budget_expense, begin_date, finish_date)
        matching_budget_expenses.update(current_occurrences)
    return matching_budget_expenses

def get_all_occurences_of_all_anticipated_income_for_dates(user, begin_date, finish_date):
    incomes = Income.objects.filter(user = user, end_date__gte = begin_date)
    matching_incomes = {}
    for income in incomes:
        current_occurrences = get_anticipated_transaction_occurences(income, begin_date, finish_date)
        matching_incomes.update(current_occurrences)
    return matching_incomes

# Returns the first bussiness day at or before the input date
def get_closest_business_day(date): 
    us_holidays = holidays.US() 
    while(date in us_holidays or not(is_weekday(date))):
        date -= timedelta(days=1)
    return date

def is_weekday(date):
    number_of_day = date.weekday()
    if number_of_day < 5:
        return True
    else:
        return False

def greater_than_or_equal_to_time_insensitive(date1, date2):
    if equal_time_insensitive(date1, date2):
        return True
    elif date1 >= date2:
        return True
    else: 
        return False

def equal_time_insensitive(date1, date2):
    if date1.day == date2.day and date1.month == date2.month and date1.year == date2.year:
        return True
    else:
        return False

def less_than_or_equal_to_time_insensitive(date1, date2):
    if equal_time_insensitive(date1, date2):
        return True
    elif date1 <= date2:
        return True
    else: 
        return False

def calculate_total_user_expense_value_in_timeperiod(user, start_date, end_date):
    budget_expenses = get_all_occurences_of_all_expenses_for_dates(user = user, begin_date = start_date, finish_date = end_date)
    amount = 0
    for expense in budget_expenses.keys(): 
        current_amount = expense.amount
        current_amount *= len(budget_expenses.get(expense))
        amount += current_amount 
    return amount

def calculate_total_user_income_value_in_timeperiod(user, start_date, end_date):
    incomes = get_all_occurences_of_all_anticipated_income_for_dates(user = user, begin_date = start_date, finish_date= end_date)
    amount = 0 
    for income in incomes.keys():
        current_amount = income.amount
        current_amount *= len(incomes.get(income))
        amount += current_amount
    return amount

def pay_day_since_last_login(user):
    last_login = user.last_login 
    if (last_login != None):
        start_date = last_login
        end_date = timezone.now()
        incomes = get_all_occurences_of_all_anticipated_income_for_dates(user, start_date, end_date)
        for income in incomes:
            occurrences = incomes.get(income)
            if len(occurrences) >= 1:
                return True
    return False

def is_pay_day(user): 
    start_date = timezone.now()
    end_date = timezone.now()
    incomes = get_all_occurences_of_all_anticipated_income_for_dates(user, start_date, end_date)
    for income in incomes:
        occurrences = incomes.get(income)
        if len(occurrences) >= 1:
            return True
    return False

