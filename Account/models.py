from django.db import models
from django.conf import settings

User=settings.AUTH_USER_MODEL
Follower = settings.AUTH_USER_MODEL

# Create your models here.
class Account(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    PUBLIC='pub'
    PRIVATE='pvt'
    Account_choices=[
        (PUBLIC,'Public'),
        (PRIVATE,'Private')
    ]
    AccountType=models.CharField(max_length=3,choices=Account_choices,default=PUBLIC)


# Create your models here.
class Relation(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    follower = models.ForeignKey(Follower,on_delete=models.CASCADE)
    isFollower = models.BooleanField(default=False)