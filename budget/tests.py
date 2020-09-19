from django.test import TestCase
from users.models import CustomUser
from budget.models import BudgetExpense, Income
from budget.models import ExpenseType
from datetime import datetime
from datetime import timedelta
from budget.services import get_all_upcoming_budget_expenses, \
                            get_all_occurences_of_all_expenses_for_dates, \
                            get_anticipated_transaction_occurences, \
                            get_last_day_of_month, \
                            is_weekday, \
                            get_closest_business_day, \
                            calculate_total_user_expense_value_in_timeperiod,\
                            get_all_upcoming_anticipated_income, \
                            get_all_occurences_of_all_anticipated_income_for_dates,\
                            calculate_total_user_income_value_in_timeperiod
from django.utils import timezone
from calendar import monthrange

class TestBudgetExpenseServices(TestCase):
    @classmethod
    def setUpTestData(cls):
        """ Set up user """
        test_user = CustomUser.objects.create_user("Test User", email="test_user_saverlife@yopmail.com",password="password", last_login = timezone.now()-timedelta(days=2))
        """ Set up expense types """
        rent_expense_type = ExpenseType.objects.create(expense_type_name="Rent")
        internet_expense_type = ExpenseType.objects.create(expense_type_name="Internet")
        car_payment_expense_type = ExpenseType.objects.create(expense_type_name="Car Payment")
        grocery_expense_type = ExpenseType.objects.create(expense_type_name = "Groceries")

        """ Set up dates """
        current_date = timezone.now()
        today_start_date = current_date if current_date.day <= 28 else current_date.replace(day=28)
        internet_start_date = today_start_date
        internet_end_date = today_start_date + timedelta(days = 90)
        rent_end_date = today_start_date + timedelta(days = 120)
        car_payment_start_date = today_start_date.replace(day = 8, month = 7, year = 2020)
        car_payment_end_date = today_start_date.replace(day = 31, month = 8, year = 2020)
        first_day_of_current_month = current_date.replace(day = 1)

        """ Set up budget expenses """
        """ Upcoming """
        """ 
        Internet Budget Expense (id=100) 
        "Today" (or the 28) if we are at the end of the month until 90 days
        Monthly
        """
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
        """ 
        Internet Budget Expense (id=100) 
        "Today"- 1 (or the 27) if we are at the end of the month until 3*365 days 
        Annually 
        """
        internet_budget_expense = BudgetExpense.objects.create(\
                                    user = test_user, \
                                    amount = 40.00, \
                                    recurrence_freq = 5, \
                                    importance = 1, \
                                    end_date = today_start_date + timedelta(days= 3*365), \
                                    start_date = today_start_date - timedelta(days = 1), \
                                    expense_type = car_payment_expense_type, \
                                    expense_name = "Annual expense name", \
                                    id = 150)

        """ 
        Rent Budget Expense (id=200)
        "Today" (or the 28) if we are at the end of the month until 120 days
        Biweekly 
        """
        rent_budget_expense = BudgetExpense.objects.create(\
                                    user = test_user, \
                                    amount = 500.00, \
                                    recurrence_freq = 2, \
                                    importance = 1, \
                                    end_date = rent_end_date, \
                                    start_date = today_start_date, \
                                    expense_type = rent_expense_type,\
                                    expense_name = "Rent expense name",\
                                    id = 200)
        """ 
        Weekly only bussiness days id = 600 
        Aug 31, 2020 (Monday) until 80 days after "today"
        Weekly
        """
        businessdays_budget_expense = BudgetExpense.objects.create( \
                                    user = test_user, \
                                    amount = 100.00, \
                                    recurrence_freq = 1, \
                                    importance = 1, \
                                    end_date = today_start_date + timedelta(days=80), \
                                    start_date = today_start_date.replace(day= 31, month=8, year= 2020), \
                                    expense_type = grocery_expense_type, \
                                    expense_name = "Bussiness days only expense name",\
                                    bussiness_days_only = True, \
                                    id = 600)
        """ 
        Biweekly only bussiness days id = 700 
        Aug 24, 2020 (Monday) until 80 days after "today"
        Biweekly
        """
        businessdays_budget_expense = BudgetExpense.objects.create( \
                                    user = test_user, \
                                    amount = 10.00, \
                                    recurrence_freq = 2, \
                                    importance = 1, \
                                    end_date = today_start_date + timedelta(days=80), \
                                    start_date = today_start_date.replace(day= 24, month=8, year= 2020), \
                                    expense_type = grocery_expense_type, \
                                    expense_name = "Bussiness days biweekly expense name",\
                                    bussiness_days_only = True, \
                                    id = 700)
        """ 
        Twice monthly rent (starting on the 1st) id = 500 
        First of current month until 90 days after "today"
        Twice monthly 
        """
        twice_monthly_budget_expense = BudgetExpense.objects.create( \
                                    user = test_user, \
                                    amount = 100.00, \
                                    recurrence_freq = 4, \
                                    importance = 1, \
                                    end_date = internet_end_date, \
                                    start_date = first_day_of_current_month, \
                                    expense_type = rent_expense_type, \
                                    expense_name = "Rent",\
                                    id = 500)

        """ 
        Monthly only bussiness days id = 800 
        August 7, 2020 Friday until 80 days after "today" or (the 28th of this month depending)
        """
        businessdays_budget_expense = BudgetExpense.objects.create( \
                                    user = test_user, \
                                    amount = 10.00, \
                                    recurrence_freq = 3, \
                                    importance = 1, \
                                    end_date = today_start_date + timedelta(days=80), \
                                    start_date = today_start_date.replace(day= 7, month=8, year= 2020), \
                                    expense_type = grocery_expense_type, \
                                    expense_name = "Bussiness days monthly expense name",\
                                    bussiness_days_only = True, \
                                    id = 800)
    
        """ Past """
        """ 
        Car Payment Expense (id=300)
        July 8, 2020 Wednesday to August 31, 2020 Monday  
        Monthly
        """
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

        """ 
        Weekly Groceries expense id = 400 
        July 8, 2020 Wednesday to August 31, 2020 Monday  
        Weekly 
        """
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
        
        """ Incomes """
        """
        Same day income 
        Begins today ends in 90 days 
        Paid weekly
        """
        same_day_income = Income.objects.create( \
                            user = test_user, \
                            amount = 500.00, \
                            recurrence_freq = 1, 
                            certainty = 1, \
                            start_date = timezone.now(),\
                            end_date = timezone.now() + timedelta(days=90), \
                            income_name = "Same day income",\
                            bussiness_days_only = False,
                            id = 100
                            )
    
    def test_same_day_occurrence(self): 
        user = CustomUser.objects.get(username="Test User")
        income = Income.objects.get(id = 100)
        expected_amount = income.amount
        start_date = timezone.now()
        end_date = timezone.now()
        actual_amount = calculate_total_user_income_value_in_timeperiod(user, start_date, end_date) 
        self.assertEquals(expected_amount, actual_amount)

    def test_calculate_value(self):
        """ 
        Calculate total in the month of August 2020
        Includes id = 400, id = 300, id = 800, id = 700, id = 600 

        id = 600
        occurs once on the 31 - $100 

        id = 700
        occurs once on the 24 - $10

        id = 800
        occurs once on the 7th - $10

        id = 300 
        occurs once on the 8th - $200

        id = 400 
        occurs 5th, 12th, 19th, 26th - $100 each
        $400

        """
        user = CustomUser.objects.get(username = "Test User")
        start_date = timezone.now().replace(day=1,month=8,year=2020)
        end_date = start_date + timedelta(days=30) 
        expected_result = 720
        actual_result = calculate_total_user_expense_value_in_timeperiod(user, start_date, end_date)
        self.assertEquals(expected_result, actual_result)

    def test_get_all_upcoming_expenses(self):
        """ 
        Can successfully pull any expenses that have not passed.
        """
        print()
        print("Get all expenses will still occur")
        user = CustomUser.objects.get(username = "Test User")
        actual_result = get_all_upcoming_budget_expenses(user = user)
        for ele in actual_result:
            print(ele)
        expected_result = [ BudgetExpense.objects.get(id=100),
                            BudgetExpense.objects.get(id=150), 
                            BudgetExpense.objects.get(id=200), 
                            BudgetExpense.objects.get(id=600), 
                            BudgetExpense.objects.get(id=700),
                            BudgetExpense.objects.get(id=500),
                            BudgetExpense.objects.get(id=800)]
        print("====================")
        print()
        self.assertEquals(expected_result, list(actual_result))

    def test_get_occurrences_monthly_mid_month(self):
        """
        Can successfully get all occurrences of a specific expense 
        Monthly Expense 
        Timeframe that begins around the same time as the bill. Extends over a month in the future.
        """
        print()
        print("Get occurrences of a monthly expense between:")
        expense = BudgetExpense.objects.get(id = 100)
        start_date = expense.start_date
        end_date = start_date + timedelta(days = 40)
        print(start_date.strftime("%B %d, %y")+" and "+end_date.strftime('%B %d, %y'))
        print("======================================")
        result = get_anticipated_transaction_occurences(anticipated_transaction= expense, start_date = start_date, end_date = end_date)
        result_dates = []
        for current_expense in result.keys():
            print(current_expense)
            print("========================")
            result_dates.extend(result.get(current_expense))
            for current_date in result_dates:
                print("Date: "+current_date.strftime("%B %d, %y %T"))
        print("======================")
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
        print(start_date.strftime("%B %d, %y")+" and "+end_date.strftime('%B %d, %y'))
        print("======================================")
        result = get_anticipated_transaction_occurences(anticipated_transaction= expense, start_date = start_date, end_date = end_date)
        result_dates = []
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

    def test_weekly_bussiness_days_only(self):
        """
        Expense is weekly beginning on a Monday.
        Bussiness days only over labor day. Until the end of September.
        Should therefore occur:
        Friday 9/4 
        Monday 9/14
        Monday 9/21
        Monday 9/28

        """
        print()
        print("Test Bussiness Days Only")
        start_date = timezone.now()
        start_date = start_date.replace(day=1, month = 9, year = 2020)
        end_date = start_date.replace(day=30)
        expense = BudgetExpense.objects.get(id = 600)

        expected_dates = []
        expected_date = expense.start_date
        expected_date = expected_date.replace(day = 4, month = 9, year = 2020)
        expected_dates.append(expected_date)
        expected_date = expected_date.replace(day = 14, month = 9, year = 2020)
        expected_dates.append(expected_date)
        expected_date = expected_date.replace(day = 21, month = 9, year = 2020)
        expected_dates.append(expected_date)
        expected_date = expected_date.replace(day = 28, month = 9, year = 2020)
        expected_dates.append(expected_date)

        print("EXPECTED")
        print("==========")
        for d in expected_dates:
            print(d)

        result = get_anticipated_transaction_occurences(expense, start_date, end_date)
        print()
        print("Actual Result")
        print("============")
        for r in result.get(expense):
            print(r)
        print()
        self.assertEquals(expected_dates, result.get(expense))

    def test_biweekly_bussiness_days_only(self):
        """
        Expense is biweekly beginning on a Monday.
        Bussiness days only over labor day. Until the end of September.
        Should therefore occur:
        Friday 9/4 
        Monday 9/21
        """
        print()
        print("Test Bussiness Days Only")
        start_date = timezone.now()
        start_date = start_date.replace(day=1, month = 9, year = 2020)
        end_date = start_date.replace(day=30)
        expense = BudgetExpense.objects.get(id = 700)

        expected_dates = []
        expected_date = expense.start_date
        expected_date = expected_date.replace(day = 4, month = 9, year = 2020)
        expected_dates.append(expected_date)
        expected_date = expected_date.replace(day = 21, month = 9, year = 2020)
        expected_dates.append(expected_date)


        print("EXPECTED")
        print("==========")
        for d in expected_dates:
            print(d)

        result = get_anticipated_transaction_occurences(expense, start_date, end_date)
        print()
        print("Actual Result")
        print("============")
        for r in result.get(expense):
            print(r)
        print()
        self.assertEquals(expected_dates, result.get(expense))
    

    def test_annual_occurences(self):
        """
        Expense annually 
        """
        print()
        print("Test Annual Expense")
        start_date = timezone.now()
        end_date = start_date.replace(year=start_date.year+2)
        expense = BudgetExpense.objects.get(id = 150)

        expected_dates = []
        expected_date = expense.start_date
        expected_date = expected_date.replace(year = expected_date.year+1)
        expected_dates.append(expected_date)
        expected_date = expected_date.replace(year = expected_date.year+1)
        expected_dates.append(expected_date)


        print("EXPECTED")
        print("==========")
        for d in expected_dates:
            print(d)

        result = get_anticipated_transaction_occurences(expense, start_date, end_date)
        print()
        print("Actual Result")
        print("============")
        for r in result.get(expense):
            print(r)
        print()
        self.assertEquals(expected_dates, result.get(expense))
    
    """
    def test_get_all_occurrences_within_timeframe(self):
        
        Test get all occurrences of all bills in the next 40 days.
        
        Will always be monthly internet and biweekly rent.

        If the current date is at the end of the month (after the 28th)
        Then the monthly start date would be the 28th and the internet bill would
        only have on occurrence. 

        The rent would have an occurrence between 13 - 11 days and then again after 14 days. 

        Otherwise the today and the start dates will be the same resulting in 2 internet bills. 

        And 3 occurrences of the biweekly rent bill. 

        
        print()
        print("Test get all occurences for all bills within time frame")
        user = CustomUser.objects.get(username = "Test User")
        start_date = timezone.now() - timedelta(days=1)
        end_date = start_date + timedelta(days = 40)
        print(start_date.strftime("%B %d, %y")+" and "+end_date.strftime('%B %d, %y'))
        print("======================================")
        result = get_all_occurences_of_all_expenses_for_dates(user = user, 
                                begin_date = start_date, 
                                finish_date = end_date)
        for expense in result.keys(): 
            print('***')
            print(expense)
            for value in result.get(expense):
                print(value)
            print('***')
            print()
        print() 
        rent_expense = BudgetExpense.objects.get(id = 200)
        internet_expense = BudgetExpense.objects.get(id = 100)
        twice_monthly_expense = BudgetExpense.objects.get(id = 500)
        rent_expense_occurrences = []
        internet_expense_occurrences = []
        if (start_date.day > 28):
            date = internet_expense.start_date + timedelta(days = get_last_day_of_month(internet_expense.start_date).day)
            internet_expense_occurrences.append(date)
            
            date = rent_expense.start_date + timedelta(days = 14)
            rent_expense_occurrences.append(date)
            date += timedelta(days = 14)
            rent_expense_occurrences.append(date)

        else: 
            date = internet_expense.start_date
            internet_expense_occurrences.append(date)
            date += timedelta(days = get_last_day_of_month(internet_expense.start_date).day)
            internet_expense_occurrences.append(date)

            date = internet_expense.start_date
            rent_expense_occurrences.append(date)
            date += timedelta(days = 14)
            rent_expense_occurrences.append(date)
            date += timedelta(days = 14)
            rent_expense_occurrences.append(date)

        expected_results = {rent_expense : rent_expense_occurrences, internet_expense :internet_expense_occurrences}
                                    #.update(get_budget_expense_occurences(twice_monthly_expense, start_date=start_date, end_date= end_date))
        twice_monthly_expense_occurrences = get_budget_expense_occurences(twice_monthly_expense,start_date=start_date, end_date= end_date ) 
        expected_results.update(twice_monthly_expense_occurrences)
        print("EXPECTED RESULT")
        print("========")
        for expense in expected_results.keys(): 
            print('***')
            print(expense)
            for value in result.get(expense):
                print(value)
            print('***')
            print()
        print() 
        self.assertEquals(expected_results, result)

    def test_get_occurences_twice_monthly(self):
        today = timezone.now() 
        start_date = today.replace(day = 17) - timedelta(days = get_last_day_of_month(today).day)
        end_date = today.replace(day = 17) + timedelta(days = get_last_day_of_month(today).day)
        expense = BudgetExpense.objects.get(id = 500)
        print()
        print("Test get all occurences for twice a month")
        print()
        expected_dates = []
        date = expense.start_date
        expected_dates.append(date)
        date = date.replace(day=15)
        expected_dates.append(date)
        date = get_last_day_of_month(date)+timedelta(days=1)
        expected_dates.append(date)
        date = date.replace(day=15)
        expected_dates.append(date)
        

        print(start_date.strftime("%B %d, %y")+" and "+end_date.strftime('%B %d, %y'))
        print("======================================")
        for current_date in expected_dates:
            print("Date: "+current_date.strftime("%B %d, %y %T"))
        print("======================")
        print()

        result = get_budget_expense_occurences(expense, start_date=start_date, end_date=end_date)
        for current_expense in result.keys(): 
            print('***')
            print(current_expense)
            for value in result.get(current_expense):
                print(value)
            print('***')
            print()
        print() 
        self.assertEquals(expected_dates, result.get(expense))
        
"""
    def test_is_weekday_true(self): 
        date = datetime(day=14, month=9, year=2020)
        self.assertTrue(is_weekday(date))
    
    def test_is_weekday_false(self): 
        date = datetime(day=12, month=9, year=2020)
        self.assertFalse(is_weekday(date))

    def test_get_closest_business_day_weekend(self):
        test_date = datetime( day=12, month=9, year=2020)
        expected_result = test_date.replace(day=11)
        self.assertEquals(expected_result, get_closest_business_day(test_date))

    def test_get_closest_business_day_christmas(self):
        test_date = datetime( day=25, month=12, year=2020)
        expected_result = test_date.replace(day=24)
        self.assertEquals(expected_result, get_closest_business_day(test_date))
    
    def test_get_closest_business_day_labor_day(self):
        test_date = datetime( day=7, month=9, year=2020)
        expected_result = test_date.replace(day=4)
        self.assertEquals(expected_result, get_closest_business_day(test_date))
    
