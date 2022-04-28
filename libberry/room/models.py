from django.db import models

class Private_Room(models.Model):
    room_id = models.AutoField(primary_key=True, null=False, unique=True)
    capacity = models.PositiveIntegerField(null=False)
    location = models.CharField(max_length=10)

