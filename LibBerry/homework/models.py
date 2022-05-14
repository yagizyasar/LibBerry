from django.db import models
from material.models import *
# Create your models here.

class Homework(models.Model):
    hw_id = models.CharField(primary_key=True,max_length=30)
    due = models.DateTimeField()



