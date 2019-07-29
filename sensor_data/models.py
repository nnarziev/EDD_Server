from django.db import models
from django.db.models.deletion import CASCADE


# Create your models here.
class acc(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp = models.BigIntegerField(default=0)
    value_x = models.TextField(blank=True, default="")
    value_y = models.TextField(blank=True, default="")
    value_z = models.TextField(blank=True, default="")
    device = models.CharField(max_length=10, default="")


class step_detector(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp = models.BigIntegerField(default=0)
    device = models.CharField(max_length=10, default="")


class significant_motion(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp = models.BigIntegerField(default=0)
    device = models.CharField(max_length=10, default="")


class stationary_dur(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp_endtime = models.BigIntegerField(default=0)
    duration = models.TextField(blank=True, default="")
    device = models.CharField(max_length=10, default="")


class unlocked_dur(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp_endtime = models.BigIntegerField(default=0)
    duration = models.TextField(blank=True, default="")
    device = models.CharField(max_length=10, default="")


class phone_calls(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp_endtime = models.BigIntegerField(default=0)
    call_type = models.TextField(blank=True, default="")
    duration = models.TextField(blank=True, default="")
    device = models.CharField(max_length=10, default="")


class light_intensity(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp = models.BigIntegerField(default=0)
    value = models.TextField(blank=True, default="")
    device = models.CharField(max_length=10, default="")


class app_usage(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp = models.BigIntegerField(default=0)
    app_name = models.TextField(blank=True, default="")
    value = models.TextField(blank=True, default="")
    device = models.CharField(max_length=10, default="")


class hrm(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp = models.BigIntegerField(default=0)
    value = models.TextField(blank=True, default="")
    device = models.CharField(max_length=10, default="")
