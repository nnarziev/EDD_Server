from django.db import models
from django.db.models.deletion import CASCADE


# Create your models here.
class Response(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    day_num = models.SmallIntegerField(default=0)
    ema_1 = models.CharField(max_length=22, default='-,-,-,-,-')
    ema_2 = models.CharField(max_length=22, default='-,-,-,-,-,-/-')
    ema_3 = models.CharField(max_length=22, default='-,-,-,-,-')
    ema_4 = models.CharField(max_length=22, default='-,-,-,-,-')
    ema_5 = models.CharField(max_length=22, default='-,-,-,-,-')
    ema_6 = models.CharField(max_length=22, default='-,-,-,-,-')
