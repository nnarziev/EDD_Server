from django.shortcuts import render
from user.models import Participant
from ema.models import Response
import sensor_data.models as models
import sensor_data.views as sensor_views
from user import views
import Tools
import csv

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from Tools import RES_BAD_REQUEST


def index(request):
    participants = Participant.objects.order_by('heartbeat_smartwatch')[:200]
    context = {
        'participants': participants
    }
    return render(request=request, template_name='index.html', context=context)


@csrf_exempt
def extract_data(request, exportCSV):
    if exportCSV:
        try:
            params = Tools.extract_post_params(request)
            if 'username' in params and 'data_src' in params:
                if not views.user_exists(params['username']):
                    return JsonResponse(data={'result': 'User does NOT exist'})
                else:
                    username = params['username']
                    data_src = params['data_src']
                    participant = Participant.objects.get(id=username)
                    try:
                        # TODO: revisit all ifs and fix them
                        response = HttpResponse(content_type='text/csv')
                        if data_src == sensor_views.SRC_ACC_SP:
                            new_raw_data = models.acc.objects.filter(username=participant).order_by('timestamp')
                            response = HttpResponse(content_type='text/csv')
                            response['Content-Disposition'] = 'attachment;filename=%s(acc).csv' % username
                            writer = csv.DictWriter(response, fieldnames=['timestamp', 'val_x', 'val_y', 'val_z', 'device'])
                            writer.writeheader()
                            for data in new_raw_data:
                                writer.writerow({'timestamp': data.timestamp, 'val_x': data.value_x, 'val_y': data.value_y, 'val_z': data.value_z, 'device': data.device})
                            return response

                        elif data_src == sensor_views.SRC_SP_STEP_DETECTOR:
                            new_raw_data = models.step_detector.objects.filter(username=participant).order_by('timestamp')[:1000000]
                            response['Content-Disposition'] = 'attachment;filename=%s(step).csv' % username
                            writer = csv.DictWriter(response, fieldnames=['timestamp'])
                            writer.writeheader()
                            for data in new_raw_data:
                                writer.writerow({'timestamp': data.timestamp})
                            return response

                        elif data_src == sensor_views.SRC_SP_SIGNIFICANT_MOTION:
                            new_raw_data = models.significant_motion.objects.filter(username=participant).order_by('timestamp')[:1000000]
                            response['Content-Disposition'] = 'attachment;filename=%s(sig_motion).csv' % username
                            writer = csv.DictWriter(response, fieldnames=['timestamp'])
                            writer.writeheader()
                            for data in new_raw_data:
                                writer.writerow({'timestamp': data.timestamp})
                            return response

                        elif data_src == sensor_views.SRC_SP_STATIONARY_DUR:
                            new_raw_data = models.stationary_dur.objects.filter(username=participant).order_by('timestamp_endtime')[:1000000]
                            response['Content-Disposition'] = 'attachment;filename=%s(stationary_dur).csv' % username
                            writer = csv.DictWriter(response, fieldnames=['timestamp_endtime', 'duration'])
                            writer.writeheader()
                            for data in new_raw_data:
                                writer.writerow({'timestamp_endtime': data.timestamp_endtime, 'duration': data.duration})
                            return response

                        elif data_src == sensor_views.SRC_SP_UNLOCKED_DUR:
                            new_raw_data = models.unlocked_dur.objects.filter(username=participant).order_by('timestamp_endtime')[:1000000]
                            response['Content-Disposition'] = 'attachment;filename=%s(unlock_dur).csv' % username
                            writer = csv.DictWriter(response, fieldnames=['timestamp_endtime', 'duration'])
                            writer.writeheader()
                            for data in new_raw_data:
                                writer.writerow({'timestamp_endtime': data.timestamp_endtime, 'duration': data.duration})
                            return response

                        elif data_src == sensor_views.SRC_SP_PHONE_CALLS:
                            new_raw_data = models.phone_calls.objects.filter(username=participant).order_by('timestamp_endtime')[:1000000]
                            response['Content-Disposition'] = 'attachment;filename=%s(phone_call_dur).csv' % username
                            writer = csv.DictWriter(response, fieldnames=['timestamp_endtime', 'type', 'duration'])
                            writer.writeheader()
                            for data in new_raw_data:
                                writer.writerow({'timestamp_endtime': data.timestamp_endtime, 'type': data.call_type, 'duration': data.duration})
                            return response

                        elif data_src == sensor_views.SRC_SP_LIGHT:
                            new_raw_data = models.light_intensity.objects.filter(username=participant).order_by('timestamp')[:1000000]
                            response['Content-Disposition'] = 'attachment;filename=%s(light).csv' % username
                            writer = csv.DictWriter(response, fieldnames=['timestamp', 'value'])
                            writer.writeheader()
                            for data in new_raw_data:
                                writer.writerow({'timestamp': data.timestamp, 'value': data.value})
                            return response

                        elif data_src == sensor_views.SRC_SP_APP_USAGE:
                            new_raw_data = models.app_usage.objects.filter(username=participant).order_by('timestamp')[:1000000]
                            response['Content-Disposition'] = 'attachment;filename=%s(app_usage).csv' % username
                            writer = csv.DictWriter(response, fieldnames=['timestamp', 'app_name', 'value'])
                            writer.writeheader()
                            for data in new_raw_data:
                                writer.writerow({'timestamp': data.timestamp, 'app_name': data.app_name, 'value': data.value})
                            return response

                        elif data_src == sensor_views.DEVICE_TYPE_WATCH:
                            new_raw_data = models.hrm.objects.filter(username=participant).order_by('timestamp')[:1000000]
                            response['Content-Disposition'] = 'attachment;filename=%s(hrm).csv' % username
                            writer = csv.DictWriter(response, fieldnames=['timestamp', 'value'])
                            writer.writeheader()
                            for data in new_raw_data:
                                writer.writerow({'timestamp': data.timestamp, 'value': data.value})
                            return response

                        elif data_src == '10':
                            ema_responses = Response.objects.filter(username=participant).order_by('day_num')
                            response['Content-Disposition'] = 'attachment;filename=%s(EMA).csv' % username
                            writer = csv.DictWriter(response, fieldnames=['day_num', 'ema1', 'ema2', 'ema3', 'ema4', 'ema5', 'ema6'])
                            writer.writeheader()
                            for ema in ema_responses:
                                writer.writerow({'day_num': ema.day_num,
                                                 'ema1': ema.ema_1,
                                                 'ema2': ema.ema_2,
                                                 'ema3': ema.ema_3,
                                                 'ema4': ema.ema_4,
                                                 'ema5': ema.ema_5,
                                                 'ema6': ema.ema_6})
                            return response
                        else:
                            return JsonResponse(data={'result': 'wrong data source number'})

                    except Exception as ex:
                        print(type(ex))
                        pass
            else:
                return JsonResponse(data={'result': 'Please, put correct username and source number'})


        except ValueError as e:
            print(str(e))
            return JsonResponse(data={'result': RES_BAD_REQUEST, 'reason': 'either username or data_src was not passed as a POST argument!'})
    else:
        return render(request=request, template_name='data_extractor.html')


def ema_per_person(request, user_id):
    ema_responses = Response.objects.filter(username=user_id).order_by('day_num', 'ema_order')[:260]
    context = {
        'username': user_id,
        'ema_responses': ema_responses
    }
    return render(request=request, template_name='ema-per-person.html', context=context)
