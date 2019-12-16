from django.db import models
from django.db.models.deletion import CASCADE


# Create your models here.
class acc_sp(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp = models.BigIntegerField(default=0)
    value_x = models.FloatField(default=0)
    value_y = models.FloatField(default=0)
    value_z = models.FloatField(default=0)
    ema_order = models.SmallIntegerField(default=0)
    day_num = models.SmallIntegerField(default=0)
    lof_value = models.FloatField(default=-1)


class acc_sw(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp = models.BigIntegerField(default=0)
    value_x = models.FloatField(default=0)
    value_y = models.FloatField(default=0)
    value_z = models.FloatField(default=0)
    ema_order = models.SmallIntegerField(default=0)
    day_num = models.SmallIntegerField(default=0)
    lof_value = models.FloatField(default=-1)


class step_detector(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp = models.BigIntegerField(default=0)
    day_num = models.SmallIntegerField(default=0)
    lof_value = models.FloatField(default=-1)


class significant_motion(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp = models.BigIntegerField(default=0)
    day_num = models.SmallIntegerField(default=0)
    lof_value = models.FloatField(default=-1)


class unlocked_dur(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp_start = models.BigIntegerField(default=0)
    timestamp_end = models.BigIntegerField(default=0)
    duration = models.IntegerField(default=0)
    day_num = models.SmallIntegerField(default=0)
    lof_value = models.FloatField(default=-1)


class stationary_dur(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp_start = models.BigIntegerField(default=0)
    timestamp_end = models.BigIntegerField(default=0)
    duration = models.IntegerField(default=0)
    day_num = models.SmallIntegerField(default=0)
    lof_value = models.FloatField(default=-1)


class phone_calls(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp_start = models.BigIntegerField(default=0)
    timestamp_end = models.BigIntegerField(default=0)
    call_type = models.TextField(blank=True, default="")
    duration = models.IntegerField(default=0)
    day_num = models.SmallIntegerField(default=0)
    lof_value = models.FloatField(default=-1)


class light_intensity(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp = models.BigIntegerField(default=0)
    value = models.FloatField(default=0.0)
    day_num = models.SmallIntegerField(default=0)
    lof_value = models.FloatField(default=-1)


class hrm(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp = models.BigIntegerField(default=0)
    value = models.FloatField(default=0.0)
    ema_order = models.SmallIntegerField(default=0)
    day_num = models.SmallIntegerField(default=0)
    lof_value = models.FloatField(default=-1)


class geofencing(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp_enter = models.BigIntegerField(default=0)
    timestamp_exit = models.BigIntegerField(default=0)
    location = models.CharField(max_length=10, default="")
    day_num = models.SmallIntegerField(default=0)
    lof_value = models.FloatField(default=-1)


class gps_locations(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp = models.BigIntegerField(default=0)
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)
    accuracy = models.FloatField(default=0.0)
    altitude = models.FloatField(default=0.0)
    day_num = models.SmallIntegerField(default=0)
    lof_value = models.FloatField(default=-1)


class activities(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp = models.BigIntegerField(default=0)
    activity_type = models.CharField(max_length=10, default="")
    confidence = models.FloatField(default=0.0)
    day_num = models.SmallIntegerField(default=0)
    lof_value = models.FloatField(default=-1)


class total_dist_covered(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp_start = models.BigIntegerField(default=0)
    timestamp_end = models.BigIntegerField(default=0)
    value = models.FloatField(default=0.0)
    ema_order = models.SmallIntegerField(default=0)
    day_num = models.SmallIntegerField(default=0)
    lof_value = models.FloatField(default=-1)


class max_dist_from_home(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp_start = models.BigIntegerField(default=0)
    timestamp_end = models.BigIntegerField(default=0)
    value = models.FloatField(default=0.0)
    ema_order = models.SmallIntegerField(default=0)
    day_num = models.SmallIntegerField(default=0)
    lof_value = models.FloatField(default=-1)


class max_dist_two_locations(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp_start = models.BigIntegerField(default=0)
    timestamp_end = models.BigIntegerField(default=0)
    value = models.FloatField(default=0.0)
    ema_order = models.SmallIntegerField(default=0)
    day_num = models.SmallIntegerField(default=0)
    lof_value = models.FloatField(default=-1)


class radius_of_gyration(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp_start = models.BigIntegerField(default=0)
    timestamp_end = models.BigIntegerField(default=0)
    value = models.FloatField(default=0.0)
    ema_order = models.SmallIntegerField(default=0)
    day_num = models.SmallIntegerField(default=0)
    lof_value = models.FloatField(default=-1)


class stddev_of_displacement(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp_start = models.BigIntegerField(default=0)
    timestamp_end = models.BigIntegerField(default=0)
    value = models.FloatField(default=0.0)
    ema_order = models.SmallIntegerField(default=0)
    day_num = models.SmallIntegerField(default=0)
    lof_value = models.FloatField(default=-1)


class num_of_dif_places(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp_start = models.BigIntegerField(default=0)
    timestamp_end = models.BigIntegerField(default=0)
    value = models.FloatField(default=0.0)
    ema_order = models.SmallIntegerField(default=0)
    day_num = models.SmallIntegerField(default=0)
    lof_value = models.FloatField(default=-1)


class audio_loudness(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp = models.BigIntegerField(default=0)
    value = models.FloatField(default=0.0)
    day_num = models.SmallIntegerField(default=0)
    lof_value = models.FloatField(default=-1)


class app_usage_stats(models.Model):
    class Meta:
        unique_together = ['username', 'package_name', 'start_timestamp']

    username = models.ForeignKey('user.Participant', on_delete=models.CASCADE)
    package_name = models.CharField(max_length=128, default='DEFAULT_APP')
    start_timestamp = models.BigIntegerField()
    end_timestamp = models.BigIntegerField()
    total_time_in_foreground = models.IntegerField()
    lof_value = models.FloatField(default=-1)

    @staticmethod
    def get_overlapping_elements(user, package_name, from_timestamp, till_timestamp):
        overlapping_elements = []

        # CASE old_start_ts == from_timestamp
        if app_usage_stats.objects.filter(username=user, package_name=package_name, start_timestamp=from_timestamp).exists():
            for usage in app_usage_stats.objects.filter(username=user, package_name=package_name, start_timestamp=from_timestamp):
                overlapping_elements += [usage]

        # CASE old_end_ts == till_timestamp
        if app_usage_stats.objects.filter(username=user, package_name=package_name, end_timestamp=till_timestamp).exists():
            for usage in app_usage_stats.objects.filter(username=user, package_name=package_name, end_timestamp=till_timestamp):
                overlapping_elements += [usage]

        # CASE: old_start_ts < from_timestamp < old_end_ts
        if app_usage_stats.objects.filter(username=user, package_name=package_name, start_timestamp__lt=from_timestamp, end_timestamp__gt=from_timestamp).exists():
            for usage in app_usage_stats.objects.filter(username=user, package_name=package_name, start_timestamp__lt=from_timestamp, end_timestamp__gt=from_timestamp):
                overlapping_elements += [usage]

        # CASE: old_start_ts < till_timestamp < old_end_ts
        if app_usage_stats.objects.filter(username=user, package_name=package_name, start_timestamp__lt=till_timestamp, end_timestamp__gt=till_timestamp).exists():
            for usage in app_usage_stats.objects.filter(username=user, package_name=package_name, start_timestamp__lt=till_timestamp, end_timestamp__gt=till_timestamp):
                overlapping_elements += [usage]

        # CASE: from_timestamp < old_start_ts & old_end_ts < till_timestamp
        if app_usage_stats.objects.filter(username=user, package_name=package_name, start_timestamp__gt=from_timestamp, end_timestamp__lt=till_timestamp).exists():
            for usage in app_usage_stats.objects.filter(username=user, package_name=package_name, start_timestamp__gt=from_timestamp, end_timestamp__lt=till_timestamp):
                overlapping_elements += [usage]

        return None if len(overlapping_elements) == 0 else overlapping_elements

    @staticmethod
    def store_usage_changes(user, package_name, end_timestamp, total_time_in_foreground):
        # the first element of the table
        if not app_usage_stats.objects.filter(username=user, package_name=package_name).exists():
            return app_usage_stats.objects.create(
                username=user,
                package_name=package_name,
                start_timestamp=end_timestamp - total_time_in_foreground,
                end_timestamp=end_timestamp,
                total_time_in_foreground=total_time_in_foreground
            )
        # next elements of the table
        else:
            last_usage = app_usage_stats.objects.filter(username=user, package_name=package_name).order_by('-end_timestamp')[0]
            start_timestamp = end_timestamp - (total_time_in_foreground - last_usage.total_time_in_foreground)
            if start_timestamp == end_timestamp:
                # print('Zero length app usage ignored: user={0}, package={1}, start_timestamp={2}, end_timestamp={3}, total_time_in_foreground={4}'.format(user,package_name,start_timestamp,end_timestamp,total_time_in_foreground))
                return None
            elif start_timestamp == last_usage.end_timestamp:
                last_usage.total_time_in_foreground = total_time_in_foreground
                last_usage.end_timestamp = end_timestamp
                last_usage.save()
            if app_usage_stats.objects.filter(username=user, start_timestamp=start_timestamp).exists():
                '''print('Duplicate app usage ignored: user={0}, package_name={1}, start_timestamp={2}, end_timestamp={3}, total_time_in_foreground={4}'.format(
                    user,
                    package_name,
                    start_timestamp,
                    end_timestamp,
                    total_time_in_foreground
                ))'''
                return None
            else:
                overlapping_elements = app_usage_stats.get_overlapping_elements(user, package_name, start_timestamp, end_timestamp)
                if overlapping_elements is None:
                    return app_usage_stats.objects.create(
                        username=user,
                        package_name=package_name,
                        start_timestamp=start_timestamp,
                        end_timestamp=end_timestamp,
                        total_time_in_foreground=total_time_in_foreground
                    )
                else:
                    min_start_timestamp = start_timestamp
                    max_end_timestamp = end_timestamp
                    max_total_time_in_foreground = total_time_in_foreground

                    for overlapping_element in overlapping_elements:
                        min_start_timestamp = min(start_timestamp, overlapping_element.start_timestamp)
                        max_end_timestamp = min(end_timestamp, overlapping_element.end_timestamp)
                        max_total_time_in_foreground = min(total_time_in_foreground, overlapping_element.total_time_in_foreground)
                        overlapping_element.delete()

                    return app_usage_stats.objects.create(
                        username=user,
                        package_name=package_name,
                        start_timestamp=min_start_timestamp,
                        end_timestamp=max_end_timestamp,
                        total_time_in_foreground=max_total_time_in_foreground
                    )


'''
class stationary_dur(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp_start = models.BigIntegerField(default=0)
    timestamp_end = models.BigIntegerField(default=0)
    duration = models.IntegerField(default=0)
    day_num = models.SmallIntegerField(default=0)

class app_usage(models.Model):
    username = models.ForeignKey('user.Participant', on_delete=CASCADE, default="")
    timestamp_start = models.BigIntegerField(default=0)
    pkg_name = models.TextField(blank=True, default="")
    app_name = models.TextField(blank=True, default="")
    duration = models.IntegerField(default=0)
    day_num = models.SmallIntegerField(default=0)
'''
