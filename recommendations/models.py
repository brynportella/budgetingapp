from django.db import models
from users.models import CustomUser
from django.utils import timezone

# Create your models here.
class Recommendation(models.Model):
    recommendation_name = models.CharField(max_length = 150)
    recommendation_description = models.TextField()
    image = models.ImageField()
    date_created = models.DateTimeField(default = timezone.now)
    def __str__(self):
        return "{}\n {}".format(self.recommendation_name, self.recommendation_description)

class RecommendationToUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    recommendation = models.ForeignKey(Recommendation, on_delete = models.RESTRICT)
    is_complete = models.BooleanField()
    is_disabled = models.BooleanField()
    date_recommended = models.DateTimeField(default = timezone.now)
    def __str__(self):
        return "{}:\n {}".format(self.recommendation, self.user) 
