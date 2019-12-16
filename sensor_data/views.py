from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import datetime

from Tools import extract_post_params, RES_FAILURE, RES_SUCCESS, RES_BAD_REQUEST, is_user_valid
from sensor_data.models import app_usage_stats
from user.models import Participant, ReceivedFilenames
import io
import csv

from . import models

# region Constants
DEVICE_TYPE_WATCH = "sw"
DEVICE_TYPE_PHONE = "sp"

SRC_ACC_SP = "1"
SRC_SP_STATIONARY_DUR = "2"
SRC_SP_SIGNIFICANT_MOTION = "3"
SRC_SP_STEP_DETECTOR = "4"
SRC_SP_UNLOCKED_DUR = "5"
SRC_SP_PHONE_CALLS = "6"
SRC_SP_LIGHT = "7"
SRC_SP_APP_USAGE = "8"
SRC_SP_GPS_LOCATIONS = "9"
SRC_SP_ACTIVITY = "10"
SRC_SP_TOTAL_DIST_COVERED = "11"
SRC_SP_MAX_DIST_FROM_HOME = "12"
SRC_SP_MAX_DIST_TWO_LOCATIONS = "13"
SRC_SP_RADIUS_OF_GYRATION = "14"
SRC_SP_STDDEV_OF_DISPLACEMENT = "15"
SRC_SP_NUM_OF_DIF_PLACES = "16"
SRC_SP_AUDIO_LOUDNESS = "17"

SRC_HRM_SW = "50"
SRC_ACC_SW = "51"

LOCATION_HOME = "HOME"
LOCATION_DORM = "DORM"
LOCATION_UNIV = "UNIV"
LOCATION_LIBRARY = "LIBRARY"
LOCATION_ADDITIONAL = "ADDITIONAL"


# endregion

@csrf_exempt
@require_http_methods(['POST'])
def submit_api(request):
    try:
        params = extract_post_params(request)

        if 'username' not in params or 'password' not in params or 'file' not in request.FILES:
            raise ValueError('username/password/file is not in request params')
        if not is_user_valid(params['username'], params['password']):
            print("Response RES_FAILURE")
            return JsonResponse({'result': RES_FAILURE})
        else:
            username = params['username']
            participant = Participant.objects.get(id=username)
            reg_time = participant.register_datetime

            csv_file = request.FILES['file']
            device_name = csv_file.name.split('_')[0]
            data_set = csv_file.read().decode('ascii')
            io_string = io.StringIO(data_set)

            print("File received", username, ";\tsize: ", len(data_set) / 1024, ";\tfilename: ", csv_file.name)

            if len(data_set) == 0:
                print("File length is 0")
                return JsonResponse(data={'result': RES_SUCCESS})

            new_filename, created = ReceivedFilenames.objects.get_or_create(username=participant, filename=csv_file.name)
            if created:
                new_filename.save()
            else:
                print("Duplicate file", new_filename.username.id, ";\tfilename: ", new_filename.filename)
                return JsonResponse(data={'result': RES_SUCCESS})

            data_src_tmp = ''
            line_num_tmp = 0
            try:
                # region Processing the received data

                file_read = csv.reader(io_string, delimiter=',', quotechar="|")

                for idx, column in enumerate(file_read):
                    data_src = column[0]
                    values = column[1]

                    data_src_tmp = data_src
                    line_num_tmp = idx

                    if data_src == SRC_ACC_SP:
                        # new_raw_data = models.acc_sp(username=participant, timestamp=timestamp, value_x=val_x, value_y=val_y, value_z=val_z, ema_order=ema_order, day_num=get_day_num(float(timestamp), reg_time))
                        elems = values.split(" ")
                        ema_order = 0
                        if len(elems) == 4:
                            # old version
                            timestamp, val_x, val_y, val_z = elems
                            pass
                        else:
                            timestamp, val_x, val_y, val_z, ema_order = elems
                        new_raw_data = models.acc_sp(username=participant, timestamp=timestamp, value_x=val_x, value_y=val_y, value_z=val_z, ema_order=ema_order, day_num=get_day_num(float(timestamp), reg_time))
                        new_raw_data.save()
                    elif data_src == SRC_ACC_SW:
                        timestamp, val_x, val_y, val_z, ema_order = values.split(" ")
                        new_raw_data = models.acc_sw(username=participant, timestamp=timestamp, value_x=val_x, value_y=val_y, value_z=val_z, ema_order=ema_order, day_num=get_day_num(float(timestamp), reg_time))
                        new_raw_data.save()
                    elif data_src == SRC_SP_STEP_DETECTOR:
                        timestamp = values
                        new_raw_data = models.step_detector(username=participant, timestamp=timestamp, day_num=get_day_num(float(timestamp), reg_time))
                        new_raw_data.save()
                    elif data_src == SRC_SP_SIGNIFICANT_MOTION:
                        timestamp = values
                        new_raw_data = models.significant_motion(username=participant, timestamp=timestamp, day_num=get_day_num(float(timestamp), reg_time))
                        new_raw_data.save()
                    elif data_src == SRC_SP_UNLOCKED_DUR:
                        start, end, duration = values.split(" ")
                        new_raw_data = models.unlocked_dur(username=participant, timestamp_start=start, timestamp_end=end, duration=duration, day_num=get_day_num(float(end), reg_time))
                        new_raw_data.save()
                    elif data_src == SRC_SP_STATIONARY_DUR:
                        start, end, duration = values.split(" ")
                        new_raw_data = models.stationary_dur(username=participant, timestamp_start=start, timestamp_end=end, duration=duration, day_num=get_day_num(float(end), reg_time))
                        new_raw_data.save()
                    elif data_src == SRC_SP_PHONE_CALLS:
                        start, end, call_type, duration = values.split(" ")
                        new_raw_data = models.phone_calls(username=participant, timestamp_start=start, timestamp_end=end, call_type=call_type, duration=duration, day_num=get_day_num(float(end), reg_time))
                        new_raw_data.save()
                    elif data_src == SRC_SP_LIGHT:
                        timestamp, value = values.split(" ")
                        new_raw_data = models.light_intensity(username=participant, timestamp=timestamp, value=value, day_num=get_day_num(float(timestamp), reg_time))
                        new_raw_data.save()
                    elif data_src == SRC_HRM_SW:
                        timestamp, value, ema_order = values.split(" ")
                        new_raw_data = models.hrm(username=participant, timestamp=timestamp, value=value, ema_order=ema_order, day_num=get_day_num(float(timestamp), reg_time))
                        new_raw_data.save()
                    elif data_src == SRC_SP_GPS_LOCATIONS:
                        timestamp, lat, lng, accuracy, altitude = values.split(" ")
                        new_raw_data = models.gps_locations(username=participant, timestamp=timestamp, lat=lat, lng=lng, accuracy=accuracy, altitude=altitude, day_num=get_day_num(float(timestamp), reg_time))
                        new_raw_data.save()
                    elif data_src == SRC_SP_ACTIVITY:
                        timestamp, activity_type, confidence = values.split(" ")
                        new_raw_data = models.activities(username=participant, timestamp=timestamp, activity_type=activity_type, confidence=confidence, day_num=get_day_num(float(timestamp), reg_time))
                        new_raw_data.save()
                    elif data_src == SRC_SP_TOTAL_DIST_COVERED:
                        start, end, value, ema_order = values.split(" ")
                        new_raw_data = models.total_dist_covered(username=participant, timestamp_start=start, timestamp_end=end, value=value, ema_order=ema_order, day_num=get_day_num(float(end), reg_time))
                        new_raw_data.save()
                    elif data_src == SRC_SP_MAX_DIST_FROM_HOME:
                        start, end, value, ema_order = values.split(" ")
                        new_raw_data = models.max_dist_from_home(username=participant, timestamp_start=start, timestamp_end=end, value=value, ema_order=ema_order, day_num=get_day_num(float(end), reg_time))
                        new_raw_data.save()
                    elif data_src == SRC_SP_MAX_DIST_TWO_LOCATIONS:
                        start, end, value, ema_order = values.split(" ")
                        new_raw_data = models.max_dist_two_locations(username=participant, timestamp_start=start, timestamp_end=end, value=value, ema_order=ema_order, day_num=get_day_num(float(end), reg_time))
                        new_raw_data.save()
                    elif data_src == SRC_SP_RADIUS_OF_GYRATION:
                        start, end, value, ema_order = values.split(" ")
                        new_raw_data = models.radius_of_gyration(username=participant, timestamp_start=start, timestamp_end=end, value=value, ema_order=ema_order, day_num=get_day_num(float(end), reg_time))
                        new_raw_data.save()
                    elif data_src == SRC_SP_STDDEV_OF_DISPLACEMENT:
                        start, end, value, ema_order = values.split(" ")
                        new_raw_data = models.stddev_of_displacement(username=participant, timestamp_start=start, timestamp_end=end, value=value, ema_order=ema_order, day_num=get_day_num(float(end), reg_time))
                        new_raw_data.save()
                    elif data_src == SRC_SP_NUM_OF_DIF_PLACES:
                        start, end, value, ema_order = values.split(" ")
                        new_raw_data = models.num_of_dif_places(username=participant, timestamp_start=start, timestamp_end=end, value=value, ema_order=ema_order, day_num=get_day_num(float(end), reg_time))
                        new_raw_data.save()
                    elif data_src == SRC_SP_AUDIO_LOUDNESS:
                        timestamp, value = values.split(" ")
                        new_raw_data = models.audio_loudness(username=participant, timestamp=timestamp, value=value, day_num=get_day_num(float(timestamp), reg_time))
                        new_raw_data.save()
                    '''
                    elif data_src == SRC_SP_STATIONARY_DUR:
                        start, end, duration = values.split(" ")
                        new_raw_data = models.stationary_dur(username=participant, timestamp_start=start, timestamp_end=end, duration=duration, day_num=get_day_num(float(end), reg_time))
                        new_raw_data.save()
                    elif data_src == SRC_SP_APP_USAGE:
                        timestamp, pkg_name, app_name, duration = values.split("||")
                        new_raw_data = models.app_usage(username=participant, timestamp_start=timestamp, pkg_name=pkg_name, app_name=app_name, value=duration, day_num=get_day_num(float(timestamp), reg_time))
                        new_raw_data.save()
                    '''
                # endregion

                # region Setting amount of data loaded by user
                cur_datetime = datetime.datetime.now()
                last_ds_phone = datetime.datetime.fromtimestamp(participant.last_ds_smartphone)
                last_ds_watch = datetime.datetime.fromtimestamp(participant.last_ds_smartwatch)

                if device_name == DEVICE_TYPE_PHONE:
                    if cur_datetime.day == last_ds_phone.day:
                        participant.daily_data_size_smartphone = participant.daily_data_size_smartphone + (len(data_set) / 1024)
                    else:
                        participant.daily_data_size_smartphone = len(data_set) / 1024
                    participant.last_ds_smartphone = cur_datetime.timestamp()
                elif device_name == DEVICE_TYPE_WATCH:
                    if cur_datetime.day == last_ds_watch.day:
                        participant.daily_data_size_smartwatch = participant.daily_data_size_smartwatch + (len(data_set) / 1024)
                    else:
                        participant.daily_data_size_smartwatch = len(data_set) / 1024
                    participant.last_ds_smartwatch = cur_datetime.timestamp()

                participant.save()
                # endregion
            except Exception as ex:
                print("Ex: ", ex)
                print("filename: ", csv_file.name, data_src_tmp, line_num_tmp)
                print("Response RES_FAILURE", username, ";\tsize: ", len(data_set) / 1024, ";\tfilename: ", csv_file.name)
                return JsonResponse({'result': RES_FAILURE})

            print("Response RES_SUCCESS", username, ";\tsize: ", len(data_set) / 1024, ";\tfilename: ", csv_file.name)
            return JsonResponse(data={'result': RES_SUCCESS})
    except ValueError as e:
        print(e)
        print("Response RES_BAD_REQUEST")
        return JsonResponse({'result': RES_BAD_REQUEST})


@csrf_exempt
@require_http_methods(['POST'])
def handle_usage_stats_submit(request):
    try:
        params = extract_post_params(request)
        if 'username' not in params or 'password' not in params or 'app_usage' not in params:
            raise ValueError('username/password/app_usage is not in request params')
        if not is_user_valid(params['username'], params['password']):
            return JsonResponse({'result': RES_FAILURE})
        else:
            username = params['username']
            participant = Participant.objects.get(id=username)
            for element in params['app_usage'].split(','):
                package_name, last_time_used, total_time_in_foreground = [int(value) if value.isdigit() else value for value in element.split(' ')]
                app_usage_stats.store_usage_changes(
                    user=participant,
                    package_name=package_name,
                    end_timestamp=last_time_used,
                    total_time_in_foreground=total_time_in_foreground
                )
            return JsonResponse(data={'result': RES_SUCCESS})
    except ValueError as e:
        print(e)
        return JsonResponse({'result': RES_BAD_REQUEST})


@csrf_exempt
@require_http_methods(['POST'])
def submit_geofencing_api(request):
    try:
        params = extract_post_params(request)
        if 'username' not in params or 'password' not in params or 'locations' not in params:
            raise ValueError('username/password/locations is not in request params')
        if not is_user_valid(params['username'], params['password']):
            return JsonResponse({'result': RES_FAILURE})
        else:
            username = params['username']
            participant = Participant.objects.get(id=username)
            reg_time = participant.register_datetime
            json_array_locations = params["locations"]
            for item in json_array_locations:
                location_id = item['id']
                time_enter = item['timestamp_enter']
                time_exit = item['timestamp_exit']

                if time_enter == 0 or time_exit == 0:
                    return JsonResponse({'result': RES_BAD_REQUEST, "message": "location enter/exit time is 0"})

                new_location = models.geofencing(username=participant, timestamp_enter=time_enter, timestamp_exit=time_exit, location=location_id, day_num=get_day_num(time_exit, reg_time))
                new_location.save()
                print("{0}, {1}, {2}".format(location_id, time_enter, time_exit))

            return JsonResponse(data={'result': RES_SUCCESS})
    except ValueError as e:
        print(e)
        return JsonResponse({'result': RES_BAD_REQUEST})


def get_day_num(new_timestamp, register_timestamp):
    new_datetime = datetime.datetime.fromtimestamp(new_timestamp / 1000)
    new_datetime_tmp = datetime.datetime(new_datetime.year, new_datetime.month, new_datetime.day)
    reg_datetime = datetime.datetime.fromtimestamp(register_timestamp)
    reg_datetime_tmp = datetime.datetime(reg_datetime.year, reg_datetime.month, reg_datetime.day)
    return (new_datetime_tmp - reg_datetime_tmp).days + 1
