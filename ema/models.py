from django.db import models
from django.db.models.deletion import CASCADE


# Create your models here.
class Response(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    day_num = models.SmallIntegerField(default=None)
    ema_order = models.SmallIntegerField(default=None)
    mood = models.SmallIntegerField(default=-1)
    sleep_hour = models.SmallIntegerField(default=-1)
    sleep_minute = models.SmallIntegerField(default=-1)
    food = models.SmallIntegerField(default=-1)
    physical_activity = models.SmallIntegerField(default=-1)
    social_activity = models.SmallIntegerField(default=-1)
    stress = models.SmallIntegerField(default=-1)
    time_expected = models.BigIntegerField(default=0)
    time_responded = models.BigIntegerField(default=0)
