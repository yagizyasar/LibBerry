from datetime import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class MainUser(models.Model):
    user = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE,related_name="user")
    balance = models.DecimalField(max_digits=7,decimal_places=2,null=False)
    registrar_id = models.ForeignKey(User,db_column="registrar_id",on_delete=models.SET_NULL,null=True,blank=True,related_name="registrar_id")

class Librarian(models.Model):
    user = models.OneToOneField(MainUser,primary_key=True,on_delete=models.CASCADE)
    specialization = models.CharField(max_length=16)

class Student(models.Model):
    user = models.OneToOneField(MainUser,primary_key=True,on_delete=models.CASCADE)
    department = models.CharField(max_length=16,null=False)
    gpa = models.DecimalField(max_digits=3,decimal_places=2,null=False)

class OutsideMember(models.Model):
    user = models.OneToOneField(MainUser,primary_key=True,on_delete=models.CASCADE)
    registration_date = models.DateField(auto_now_add=True,null=False,blank=True)
    card_no = models.IntegerField(unique=True,null=False)
    expire_date = models.DateField(null=False,default=datetime.now()) # default değer yanlış

class Instructor(models.Model):
    user = models.OneToOneField(MainUser,primary_key=True,on_delete=models.CASCADE)
    office = models.CharField(max_length=8,null=False)
    department = models.CharField(max_length=4,null=False)
    class tenures(models.TextChoices):
        PROF = 'Prof', _('Professor')
        ASSOC_PROF = 'Assoc. Prof', _('Assoc Prof')
        ASST_PROF = 'Asst. Prof', _('Asst Prof')
        INST = 'Inst', _('Instructor')

    tenure = models.CharField(
        max_length=20,
        choices=tenures.choices,
        null = True
    )
    





    