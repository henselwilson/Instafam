from django.db import models
from django.conf import settings
from Account.models import Account
User = settings.AUTH_USER_MODEL
Follower = settings.AUTH_USER_MODEL

# Create your models here.
class Relation(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    follower = models.ForeignKey(Follower,on_delete=models.CASCADE)
    isFollower = models.BooleanField(default=False)
