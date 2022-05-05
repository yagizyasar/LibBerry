from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User,Librarian


class NewMaterialRequest(models.Model):
    request_id = models.AutoField(primary_key=True,null=False,unique=True)
    new_mat_title = models.CharField(max_length=50,null=False)
    new_mat_author = models.CharField(max_length=50,null=False)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    librarian = models.ForeignKey(Librarian,on_delete=models.SET_NULL,null=True)
    is_custom = models.BooleanField(default=False,null=False)
    description = models.TextField(max_length=300)
    class statuses(models.TextChoices):
        CONSIDER = 'in_consideration', _('in_consideration')
        ACCEPTED = 'accepted', _('accepted')
        DENIED = 'denied', _('denied')
        COMPLETED = 'completed', _('completed')

    status = models.CharField(
        max_length=20,
        choices=statuses.choices,
        default=statuses.CONSIDER,
        null=False
    )

class AskRequest(models.Model):
    ask_id = models.AutoField(primary_key=True,null=False,unique=True)
    student = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    question = models.TextField(max_length=250,null=False)
    librarian = models.ForeignKey(Librarian,on_delete=models.SET_NULL,null=True)
    reply = models.TextField(max_length=250)
    class statuses(models.TextChoices):
        UNANSWERED = 'unanswered', _('unanswered')
        ANSWERED = 'answered', _('answered')

    status = models.CharField(
        max_length=20,
        choices=statuses.choices,
        default=statuses.UNANSWERED,
        null=False
    )
    


