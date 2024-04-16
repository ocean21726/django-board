from django.db import models

# Create your models here.

class Board(models.Model):
    title = models.CharField(max_length=100)
    contents = models.CharField(max_length=2000)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(default="")
    
    def __str__(self):
        return self.name