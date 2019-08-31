from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from Tools import extract_post_params
from user.models import Participant
from ema.models import Response
from . import models
import datetime

# region Constants
RES_SUCCESS = 0
RES_FAILURE = 1
RES_BAD_REQUEST = -1


# endregion


# Create your views here.
def user_exists(username):
    return models.Participant.objects.filter(username=username).exists()


def is_user_valid(username, password):
    if user_exists(username):
        user = models.Participant.objects.get(username=username)
        return user.password == password
    return False


@csrf_exempt
@require_http_methods(['POST'])
def register_api(request):
    try:
        params = extract_post_params(request)
        if 'username' in params and 'password' in params and 'phone_num' in params and 'device_info' in params:
            username = params['username']
            phone = params['phone_num']
            device_info = params['device_info']
            password = params['password']
            print('-------------- Sign Up -------------')
            print("User: ", username, "\tPassword: ", password)

            now_date = datetime.datetime.now()

            if user_exists(username):
                return JsonResponse(data={
                    'result': RES_FAILURE, 'reason': 'username is taken'
                })
            else:
                # create a new participant
                new_participant = models.Participant(username=username,
                                                     phone_num=phone,
                                                     device_info=device_info,
                                                     password=password,
                                                     register_datetime=now_date.timestamp(),
                                                     heartbeat_smartwatch=now_date.timestamp(),
                                                     heartbeat_smartphone=now_date.timestamp())
                new_participant.save()

                ema_hours = [7, 10, 13, 16, 19, 22] # expected hours for ema responses

                # create EMA entries for this user
                for day in range(1, 32):
                    for order in range(1, 7):
                        now_date = now_date.replace(hour=ema_hours[order-1], minute=0, second=0, microsecond=0)
                        ema_user_data = Response(username=new_participant, day_num=day, ema_order=order, time_expected=now_date.timestamp())
                        ema_user_data.save()
                    now_date = now_date + datetime.timedelta(days=1)

                return JsonResponse(data={'result': RES_SUCCESS})
    except ValueError as e:
        print(str(e))
        return JsonResponse(data={'result': RES_BAD_REQUEST, 'reason': 'either username or phone number or password was not passed as a POST argument!'})


@csrf_exempt
@require_http_methods(['POST'])
def login_api(request):
    try:
        params = extract_post_params(request)
        if 'username' in params and 'password' in params:
            username = params['username']
            password = params['password']
            print('-------------- Sign In -------------')
            print("User: ", username, "\tPassword: ", password)
            if is_user_valid(username, password):
                participant = Participant.objects.get(username=username)
                participant.last_login_datetime = datetime.datetime.now().timestamp()
                participant.save()
                return JsonResponse(data={'result': RES_SUCCESS})
            else:
                return JsonResponse(data={
                    'result': RES_FAILURE, 'reason': 'wrong credentials passed'
                })
    except ValueError as e:
        print(str(e))
        return JsonResponse(data={'result': RES_BAD_REQUEST, 'reason': 'Username or Password was not passed as a POST argument!'})


@csrf_exempt
@require_http_methods(['POST'])
def heartbeat_smartphone_api(request):
    try:
        params = extract_post_params(request)
        if 'username' in params and 'password' in params:
            username = params['username']
            password = params['password']
            if is_user_valid(username, password):
                participant = Participant.objects.get(username=username)
                participant.heartbeat_smartphone = datetime.datetime.now().timestamp()
                participant.save()
                return JsonResponse(data={'result': RES_SUCCESS})
            else:
                return JsonResponse(data={
                    'result': RES_FAILURE, 'reason': 'wrong credentials passed'
                })
    except ValueError as e:
        print(str(e))
        return JsonResponse(data={'result': RES_BAD_REQUEST, 'reason': 'Username or Password was not passed as a POST argument!'})


@csrf_exempt
@require_http_methods(['POST'])
def heartbeat_smartwatch_api(request):
    try:
        params = extract_post_params(request)
        if 'username' in params and 'password' in params:
            username = params['username']
            password = params['password']
            if is_user_valid(username, password):
                participant = Participant.objects.get(username=username)
                participant.heartbeat_smartwatch = datetime.datetime.now().timestamp()
                participant.save()
                return JsonResponse(data={'result': RES_SUCCESS})
            else:
                return JsonResponse(data={
                    'result': RES_FAILURE, 'reason': 'wrong credentials passed'
                })
    except ValueError as e:
        print(str(e))
        return JsonResponse(data={'result': RES_BAD_REQUEST, 'reason': 'Username or Password was not passed as a POST argument!'})


@csrf_exempt
@require_http_methods(['POST'])
def get_user_stat_api(request):
    try:
        params = extract_post_params(request)
        if 'username' in params and 'password' in params:
            username = params['username']
            password = params['password']
            if is_user_valid(username, password):
                participant_obj = Participant.objects.get(username=username)

                # User stats variables
                current_day_num = participant_obj.current_day_num()
                ema_counter = 0  # num of responded emas for that day
                last_hb_watch = participant_obj.heartbeat_smartwatch_diff_min()  # in minutes
                last_hb_phone = participant_obj.heartbeat_smartphone_diff_min()  # in minutes
                data_loaded_watch = participant_obj.watch_data_size()
                data_loaded_phone = participant_obj.phone_data_size()

                # region Number of ema responses
                ema_obj = Response.objects.filter(username=participant_obj, day_num=current_day_num)

                for ema in ema_obj:
                    if ema.time_responded != 0:
                        ema_counter += 1

                return JsonResponse(data={'result': RES_SUCCESS,
                                          'day_number': current_day_num,
                                          'ema_responses_number': ema_counter,
                                          'heartbeat_watch': last_hb_watch,
                                          'heartbeat_phone': last_hb_phone,
                                          'data_loaded_watch': data_loaded_watch,
                                          'data_loaded_phone': data_loaded_phone})
            else:
                return JsonResponse(data={
                    'result': RES_FAILURE, 'reason': 'wrong credentials passed'
                })
    except ValueError as e:
        print(str(e))
        return JsonResponse(data={'result': RES_BAD_REQUEST, 'reason': 'Username or Password was not passed as a POST argument!'})
