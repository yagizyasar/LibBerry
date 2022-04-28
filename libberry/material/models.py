from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _  

class Material(models.Model):
    mat_id = models.AutoField(primary_key=True, null=False, unique=True)
    title = models.CharField(max_length=50, null=False)
    genre = models.CharField(max_length=50, null=False)
    publish_date = models.DateField(null=False)
    amount = models.IntegerField(null=False)
    location = models.CharField(max_length=10)

class Printed(models.Model):
    mat_id = models.ForeignKey(Material, on_delete=models.CASCADE, primary_key=True)
    pages = models.IntegerField()

class Audiovisual(models.Model):

    # Constraint interval
    # def validate_interval(value):
    #    if value < 0.0 or value > 10.0:
    #       raise ValidationError(_('%(value)s must be in the range [0.0, 10.0]'), params={'value': value},)

    mat_id = models.ForeignKey(Material, on_delete=models.CASCADE, primary_key=True)
    external_rating = models.DecimalField(max_digits=3,decimal_places=2)
    length = models.TimeField()

class Periodical_Material(models.Model):
    mat_id = models.ForeignKey(Material, on_delete=models.CASCADE, primary_key=True)
    pages = models.IntegerField()
    period = models.CharField(max_length=12)

class Material_Set(models.Model):
    set_id = models.AutoField(primary_key=True, null=False, unique=True)
    publicity = 
