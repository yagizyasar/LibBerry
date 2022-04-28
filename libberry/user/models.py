from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    user_id = models.AutoField(primary_key=True,unique=True,null=False)
    password = models.CharField(max_length=100,null=False)
    name = models.CharField(max_length=50,null=False)
    surname = models.CharField(max_length=32,null=False)
    balance = models.DecimalField(max_digits=7,decimal_places=2,null=False)
    email = models.EmailField(max_length=254,null=False,unique=True)
    registrar_id = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True)

class Librarian(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=False,primary_key=True)
    specialization = models.CharField(max_length=16)

class Student(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=False,primary_key=True)
    department = models.CharField(max_length=16,null=False)
    gpa = models.DecimalField(max_digits=3,decimal_places=2,null=False)

class OutsideMember(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=False,primary_key=True)
    registration_date = models.DateField(auto_now_add=True,null=False)
    card_no = models.IntegerField(unique=True,null=False)

class Instructor(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=False,primary_key=True)
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
    


    






    