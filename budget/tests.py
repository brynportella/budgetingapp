from django.test import TestCase
from users.models import CustomUser
from budget.models import BudgetExpense
from budget.models import ExpenseType
from datetime import datetime
from datetime import timedelta
from budget.services import get_all_upcoming_budget_expenses
from django.utils import timezone

# Create your tests here.
class TestBudgetExpenseServices(TestCase):
    def setUp(self):
        """ Set up user """
        test_user = CustomUser.objects.create_user("Test User", email="test_user_saverlife@yopmail.com",password="password")
        """ Set up expense types """
        rent_expense_type = ExpenseType.objects.create(expense_type_name="Rent")
        internet_expense_type = ExpenseType.objects.create(expense_type_name="Internet")
        car_payment_expense_type = ExpenseType.objects.create(expense_type_name="Car Payment")

        """ Set up dates """
        today_start_date = timezone.now()
        internet_end_date = today_start_date + timedelta(days = 90)
        rent_end_date = today_start_date + timedelta(days = 120)
        car_payment_start_date = today_start_date - timedelta(days = 90)
        car_payment_end_date = today_start_date - timedelta(days = 2)

        """ Set up budget expenses """
        internet_budget_expense = BudgetExpense.objects.create(\
                                    user = test_user, \
                                    amount = 40.00, \
                                    recurrence_freq = 3, \
                                    importance = 1, \
                                    end_date = internet_end_date, \
                                    start_date = today_start_date, \
                                    expense_type = internet_expense_type)

        rent_budget_expense = BudgetExpense.objects.create(\
                                    user = test_user, \
                                    amount = 500.00, \
                                    recurrence_freq = 3, \
                                    importance = 1, \
                                    end_date = rent_end_date, \
                                    start_date = today_start_date, \
                                    expense_type = rent_expense_type)

        car_payment_budget_expense = BudgetExpense.objects.create( \
                                    user = test_user, \
                                    amount = 200.00, \
                                    recurrence_freq = 3, \
                                    importance = 1, \
                                    end_date = car_payment_end_date, \
                                    start_date = car_payment_start_date, \
                                    expense_type = car_payment_expense_type)

    def test_get_all_upcoming_expenses(self):
        """ 
        Can successfully pull any expenses that have not passed.
        """
        result = get_all_upcoming_budget_expenses()
        for ele in result:
            print(ele)
        
        self.assertEquals([], result)
