from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class User_table(models.Model):
    LOGIN = models.ForeignKey(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)
    DOB = models.DateField()
    Gender = models.CharField(max_length=15)
    Photo = models.FileField()
    Place = models.CharField(max_length=50)
    Post = models.CharField(max_length=50)
    Pin = models.IntegerField()
    Phone = models.BigIntegerField()
    Email = models.CharField(max_length=50)

class Task(models.Model):
    User = models.ForeignKey(User_table, on_delete=models.CASCADE)
    Title = models.CharField(max_length=100)
    Description = models.CharField(max_length=500)
    Priority = models.CharField(max_length=15)
    Created_date = models.DateField()
    Due_date = models.DateField()
    Status = models.CharField(max_length=20)
