from django.db import models
from users.models import CustomUser
from django.utils import timezone


# Create your models here.

class GoalType(models.Model):
    class GoalCategory(models.TextChoices):
        SAVING = 'SAVING'
        PAYING_DOWN_DEBT = 'PAYING_DOWN_DEBT'
        INVESTING = 'INVESTING'
    goal_category = models.CharField(
        max_length = 100,
        choices = GoalCategory.choices
    )
    goal_name = models.CharField(max_length = 100)
    goal_description = models.TextField()
    is_private = models.BooleanField()
    user = models.ForeignKey(CustomUser, null = True, blank = True, on_delete = models.CASCADE)
    def __str__(self):
        return GoalType.GoalCategory(self.goal_category).label+": "+self.goal_name

class Goal(models.Model):
    goal_type = models.ForeignKey(GoalType, on_delete  = models.RESTRICT)
    goal_reason = models.TextField()
    amount = models.DecimalField(max_digits=30, decimal_places=2, null=False)
    progress = models.DecimalField(max_digits=30, decimal_places=2, null=False)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    start_date = models.DateTimeField(default = timezone.now)
    end_date = models.DateTimeField()
