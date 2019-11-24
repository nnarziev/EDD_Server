from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from Tools import extract_post_params, RES_FAILURE, RES_SUCCESS, RES_BAD_REQUEST, user_exists, is_user_valid
from ema.views import EMA_HOURS, NUMBER_OF_EMA
from user.models import Participant
from ema.models import Response

from . import models
import datetime

# region Constants
EXPERIMENT_DURATION = 65  # in days


# endregion


@csrf_exempt
@require_http_methods(['POST'])
def register_api(request):
    try:
        params = extract_post_params(request)
        if 'username' in params and 'password' in params and 'phone_num' in params and 'device_info' in params:
            username = params['username']
            phone = params['phone_num']
            name = params['name']
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
                new_participant = models.Participant(id=username,
                                                     phone_num=phone,
                                                     name=name,
                                                     device_info=device_info,
                                                     password=password,
                                                     register_datetime=now_date.timestamp(),
                                                     heartbeat_smartwatch=now_date.timestamp(),
                                                     heartbeat_smartphone=now_date.timestamp())
                new_participant.save()

                # create EMA entries for this user
                for day in range(1, EXPERIMENT_DURATION + 1):
                    for order in range(1, NUMBER_OF_EMA + 1):
                        now_date = now_date.replace(hour=EMA_HOURS[order - 1], minute=0, second=0, microsecond=0)
                        ema_user_data = Response(username=new_participant, day_num=day, ema_order=order, time_expected=now_date.timestamp())
                        ema_user_data.save()
                    now_date = now_date + datetime.timedelta(days=1)

                return JsonResponse(data={'result': RES_SUCCESS})
        else:
            return JsonResponse(data={'result': RES_BAD_REQUEST})
    except Exception or ValueError as e:
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
                participant = Participant.objects.get(id=username)
                participant.last_login_datetime = datetime.datetime.now().timestamp()
                participant.save()
                return JsonResponse(data={'result': RES_SUCCESS})
            else:
                return JsonResponse(data={
                    'result': RES_FAILURE, 'reason': 'wrong credentials passed'
                })
        else:
            return JsonResponse(data={'result': RES_BAD_REQUEST})
    except Exception or ValueError as e:
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
                print("Heartbeat phone: ", username)
                participant = Participant.objects.get(id=username)
                participant.heartbeat_smartphone = datetime.datetime.now().timestamp()
                participant.save()
                return JsonResponse(data={'result': RES_SUCCESS})
            else:
                return JsonResponse(data={
                    'result': RES_FAILURE, 'reason': 'wrong credentials passed'
                })
        else:
            return JsonResponse(data={'result': RES_BAD_REQUEST})
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
                print("Heartbeat watch: ", username)
                participant = Participant.objects.get(id=username)
                participant.heartbeat_smartwatch = datetime.datetime.now().timestamp()
                participant.save()
                return JsonResponse(data={'result': RES_SUCCESS})
            else:
                return JsonResponse(data={
                    'result': RES_FAILURE, 'reason': 'wrong credentials passed'
                })
        else:
            return JsonResponse(data={'result': RES_BAD_REQUEST})
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
                participant = Participant.objects.get(id=username)
                # User stats variables
                current_day_num = participant.current_day_num()
                ema_counter = 0  # num of responded emas for that day
                last_hb_watch = participant.heartbeat_smartwatch_diff_min()  # in minutes
                last_hb_phone = participant.heartbeat_smartphone_diff_min()  # in minutes
                data_loaded_watch = participant.watch_data_size()
                data_loaded_phone = participant.phone_data_size()

                # region Number of ema responses
                # ema_obj = Response.objects.filter(username=participant_obj, day_num=current_day_num)

                ema_responses = Response.objects.filter(username=participant, day_num=current_day_num).order_by('time_expected')
                ema_resp = []
                mood_data = []
                for ema in ema_responses:
                    if ema.time_responded != 0:
                        ema_resp += ['1']
                        mood_data += [ema.mood]
                        ema_counter += 1
                    else:
                        ema_resp += ['0']

                return JsonResponse(data={'result': RES_SUCCESS,
                                          'day_number': current_day_num,
                                          'ema_responses_number': ema_counter,
                                          'ema_responses': ema_resp,
                                          'heartbeat_watch': last_hb_watch,
                                          'heartbeat_phone': last_hb_phone,
                                          'data_loaded_watch': data_loaded_watch,
                                          'data_loaded_phone': data_loaded_phone,
                                          'mood_data': mood_data})
            else:
                return JsonResponse(data={
                    'result': RES_FAILURE, 'reason': 'wrong credentials passed'
                })
        else:
            return JsonResponse(data={'result': RES_BAD_REQUEST})
    except ValueError as e:
        print(str(e))
        return JsonResponse(data={'result': RES_BAD_REQUEST, 'reason': 'Username or Password was not passed as a POST argument!'})
