from django.db import models

class Resource(models.Model):
    image_url = models.URLField(max_length = 300)
    resource_title = models.CharField(max_length = 150)
    # Alt text for the image
    resource_description = models.TextField() 
    resource_url = models.URLField(max_length = 300)
    def __str__(self):
        return self.resource_title


