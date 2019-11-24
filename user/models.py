from django.db import models
import datetime
from string import Template
from django.db.models.deletion import CASCADE


# Create your models here.

class DeltaTemplate(Template):
    delimiter = "%"


class Participant(models.Model):
    id = models.CharField(max_length=25, primary_key=True)
    email = models.CharField(max_length=25, default="")
    name = models.CharField(max_length=25, default="")
    phone_num = models.CharField(default="", max_length=16)
    device_info = models.TextField(blank=True, default="")
    password = models.CharField(max_length=16)
    register_datetime = models.BigIntegerField(default=datetime.datetime.now().timestamp())
    last_login_datetime = models.BigIntegerField(default=datetime.datetime.now().timestamp())
    heartbeat_smartwatch = models.BigIntegerField(default=datetime.datetime.now().timestamp())
    heartbeat_smartphone = models.BigIntegerField(default=datetime.datetime.now().timestamp())
    daily_data_size_smartwatch = models.FloatField(default=0)
    daily_data_size_smartphone = models.FloatField(default=0)
    last_ds_smartphone = models.BigIntegerField(default=datetime.datetime.now().timestamp())
    last_ds_smartwatch = models.BigIntegerField(default=datetime.datetime.now().timestamp())
    type = models.CharField(default="", max_length=10)

    def heartbeat_smartwatch_diff(self):
        time_dif = (datetime.datetime.now() - datetime.datetime.fromtimestamp(self.heartbeat_smartwatch))
        # return strfdelta(time_dif, "%D days %H:%M")
        return time_dif - datetime.timedelta(microseconds=time_dif.microseconds)

    def heartbeat_smartphone_diff(self):
        time_dif = (datetime.datetime.now() - datetime.datetime.fromtimestamp(self.heartbeat_smartphone))
        return time_dif - datetime.timedelta(microseconds=time_dif.microseconds)

    def last_ds_smartphone_diff(self):
        time_dif = (datetime.datetime.now() - datetime.datetime.fromtimestamp(self.last_ds_smartphone))
        return time_dif - datetime.timedelta(microseconds=time_dif.microseconds)

    def last_ds_smartwatch_diff(self):
        time_dif = (datetime.datetime.now() - datetime.datetime.fromtimestamp(self.last_ds_smartwatch))
        return time_dif - datetime.timedelta(microseconds=time_dif.microseconds)

    def heartbeat_smartwatch_diff_min(self):
        time_dif = (datetime.datetime.now() - datetime.datetime.fromtimestamp(self.heartbeat_smartwatch))
        # return strfdelta(time_dif, "%D days %H:%M")
        return time_dif.total_seconds() / 60

    def heartbeat_smartphone_diff_min(self):
        time_dif = (datetime.datetime.now() - datetime.datetime.fromtimestamp(self.heartbeat_smartphone))
        return time_dif.total_seconds() / 60

    def register_date(self):
        return datetime.datetime.fromtimestamp(self.register_datetime)

    def current_day_num(self):
        cur_datetime = datetime.datetime.now()
        cur_datetime_tmp = datetime.datetime(cur_datetime.year, cur_datetime.month, cur_datetime.day)
        reg_datetime = datetime.datetime.fromtimestamp(self.register_datetime)
        reg_datetime_tmp = datetime.datetime(reg_datetime.year, reg_datetime.month, reg_datetime.day)
        return (cur_datetime_tmp - reg_datetime_tmp).days + 1

    def watch_data_size(self):
        return "{0:.2f}".format(round(self.daily_data_size_smartwatch / 1024, 2))

    def phone_data_size(self):
        return "{0:.2f}".format(round(self.daily_data_size_smartphone / 1024, 2))

    '''
    def strfdelta(tdelta, fmt):
        d = {"D": tdelta.days}
        d["H"], rem = divmod(tdelta.seconds, 3600)
        d["M"], d["S"] = divmod(rem, 60)
        t = DeltaTemplate(fmt)
        return t.substitute(**d)
    '''


class ReceivedFilenames(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    filename = models.CharField(max_length=22)