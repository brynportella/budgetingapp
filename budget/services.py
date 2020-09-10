from .models import ExpenseType
from .models import BudgetExpense
from django.utils import timezone

def get_all_upcoming_budget_expenses():
    return BudgetExpense.objects.filter(end_date__gte = timezone.now())