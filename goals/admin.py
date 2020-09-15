from django.contrib import admin
from .models import GoalType, Goal
# Register your models here.

admin.site.register(GoalType)
admin.site.register(Goal)