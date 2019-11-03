from django.db import models
from django.db.models.deletion import CASCADE


# Create your models here.
class Response(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    day_num = models.SmallIntegerField(default=None)
    ema_order = models.SmallIntegerField(default=None)
    interest = models.SmallIntegerField(default=-1)
    mood = models.SmallIntegerField(default=-1)
    sleep = models.SmallIntegerField(default=-1)
    fatigue = models.SmallIntegerField(default=-1)
    weight = models.SmallIntegerField(default=-1)
    worthlessness = models.SmallIntegerField(default=-1)
    concentrate = models.SmallIntegerField(default=-1)
    restlessness = models.SmallIntegerField(default=-1)
    suicide = models.SmallIntegerField(default=-1)
    time_expected = models.BigIntegerField(default=0)
    time_responded = models.BigIntegerField(default=0)
    lof_value = models.FloatField(default=-1)