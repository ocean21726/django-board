from django.db import models

# Create your models here.

class Board(models.Model):
    idx = models.AutoField(primary_key=True, null=False)
    title = models.CharField(max_length=100)
    contents = models.CharField(max_length=2000)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.name