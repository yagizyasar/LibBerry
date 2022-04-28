from django.db import models
from user.models import User, Librarian
from material.models import Material

class Warning(models.Model):
    warn_id = models.AutoField(primary_key=True, null=False, unique=True)
    user_id = models.ForeignKey(User,  on_delete=models.CASCADE)
    librarian_id = models.ForeignKey(Librarian,  on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    sent_datetime = models.DateTimeField(null=False)

class Nearly_Due_Warning(models.Model):
    warn_id = models.ForeignKey(Warning,  on_delete=models.CASCADE, primary_key=True)
    mat_id = models.ForeignKey(Material,  on_delete=models.CASCADE)
    remaining_days = models.BigIntegerField(null=False)
    

# Create your models here.
