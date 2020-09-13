from django.test import TestCase
from users.models import CustomUser
from budget.models import BudgetExpense
from budget.models import ExpenseType
from datetime import datetime
from datetime import timedelta
from budget.services import get_all_upcoming_budget_expenses
from budget.services import get_budget_expense_occurences
from django.utils import timezone
from calendar import monthrange

# Create your tests here.
class TestBudgetExpenseServices(TestCase):
    def setUp(self):
        """ Set up user """
        test_user = CustomUser.objects.create_user("Test User", email="test_user_saverlife@yopmail.com",password="password")
        """ Set up expense types """
        rent_expense_type = ExpenseType.objects.create(expense_type_name="Rent")
        internet_expense_type = ExpenseType.objects.create(expense_type_name="Internet")
        car_payment_expense_type = ExpenseType.objects.create(expense_type_name="Car Payment")
        grocery_expense_type = ExpenseType.objects.create(expense_type_name = "Groceries")

        """ Set up dates """
        today_start_date = timezone.now()
        internet_end_date = today_start_date + timedelta(days = 90)
        rent_end_date = today_start_date + timedelta(days = 120)
        car_payment_start_date = today_start_date - timedelta(days = 90)
        car_payment_end_date = today_start_date - timedelta(days = 2)

        """ Set up budget expenses """
        """ Internet Budget Expense (id=100) """
        internet_budget_expense = BudgetExpense.objects.create(\
                                    user = test_user, \
                                    amount = 40.00, \
                                    recurrence_freq = 3, \
                                    importance = 1, \
                                    end_date = internet_end_date, \
                                    start_date = today_start_date, \
                                    expense_type = internet_expense_type, \
                                    expense_name = "Internet expense name", \
                                    id = 100)

        """ Rent Budget Expense (id=200) """
        rent_budget_expense = BudgetExpense.objects.create(\
                                    user = test_user, \
                                    amount = 500.00, \
                                    recurrence_freq = 3, \
                                    importance = 1, \
                                    end_date = rent_end_date, \
                                    start_date = today_start_date, \
                                    expense_type = rent_expense_type,\
                                    expense_name = "Rent expense name",\
                                    id = 200)
        
        """ Car Paymeent Expense (id=300) """
        car_payment_budget_expense = BudgetExpense.objects.create( \
                                    user = test_user, \
                                    amount = 200.00, \
                                    recurrence_freq = 3, \
                                    importance = 1, \
                                    end_date = car_payment_end_date, \
                                    start_date = car_payment_start_date, \
                                    expense_type = car_payment_expense_type, \
                                    expense_name = "Car payment expense name",\
                                    id = 300)
        """ Weekly Groceries expense id = 400 """
        grocery_budget_expense = BudgetExpense.objects.create( \
                                    user = test_user, \
                                    amount = 100.00, \
                                    recurrence_freq = 1, \
                                    importance = 1, \
                                    end_date = car_payment_end_date, \
                                    start_date = car_payment_start_date, \
                                    expense_type = grocery_expense_type, \
                                    expense_name = "Grocery expense name",\
                                    id = 400)
    def test_get_all_upcoming_expenses(self):
        """ 
        Can successfully pull any expenses that have not passed.
        """
        user = CustomUser.objects.get(username = "Test User")
        actual_result = get_all_upcoming_budget_expenses(user = user)
        for ele in actual_result:
            print(ele)
        expected_result = [BudgetExpense.objects.get(id=100), BudgetExpense.objects.get(id=200)]
        print()
        self.assertEquals(expected_result, list(actual_result))

    def test_get_occurrences_monthly_mid_month(self):
        """
        Can successfully get all occurrences of a specific expense
        """
        print("Get monthly occurrences")
        expense = BudgetExpense.objects.get(id = 100)
        start_date = expense.start_date
        end_date = start_date + timedelta(days = 40)
        result = get_budget_expense_occurences(expense = expense, start_date = start_date, end_date = end_date)
        result_dates = []
        for current_expense in result.keys():
            print(current_expense)
            result_dates.extend(result.get(current_expense))
            for current_date in result_dates:
                print(current_date)
        print()
        date_1 = start_date
        days_in_month = monthrange(start_date.year, start_date.month)[1]
        date_2 = start_date + timedelta(days = days_in_month)
        
        self.assertEquals([date_1, date_2], result_dates)

    def test_get_occurences_weekly(self):
        """
        Based on an expense that occurs weekly get all occurences within a 
        particular time frame
        """
        print("Get weekly occurrences")
        expense = BudgetExpense.objects.get(id = 400)
        start_date = expense.start_date
        end_date = start_date + timedelta(days = 40)
        result = get_budget_expense_occurences(expense = expense, start_date = start_date, end_date = end_date)
        result_dates = []
        print("End date "+end_date.__str__())
        print("Expense end date "+expense.end_date.__str__())
        for current_expense in result.keys():
            print(current_expense)
            result_dates.extend(result.get(current_expense))
            for current_date in result_dates:
                print(current_date)
        print()
        expected_dates = []
        current_date = start_date
        while current_date < end_date: 
            expected_dates.append(current_date)
            current_date += timedelta(days =  7)

        self.assertEquals(expected_dates, result_dates)