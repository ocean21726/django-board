from django.db import models

# Create your models here.

class Member(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    