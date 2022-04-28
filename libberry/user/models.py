from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=32,null=False)
    name = models.CharField(max_length=32,null=False)
    surname = models.CharField(max_length=32,null=False)
    balance = models.DecimalField(max_digits=7,decimal_places=2)
    email = models.EmailField(max_length=254,null=False)
    
    class Meta:
        abstract = True
    