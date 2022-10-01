from django.db import models

# Create your models here.


class Organization(models.Model):

    name = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField(("logo of the organization"), )
    website  = models.URLField(("website of the organization"), max_length=200)
    location = models.CharField(max_length=255, null=True, blank=True)
    googlemap_link = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
            return self.name
    
    

