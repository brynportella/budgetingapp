from django.contrib import admin
from .models import Recommendation, RecommendationToUser

# Register your models here.
admin.site.register(Recommendation)
admin.site.register(RecommendationToUser)