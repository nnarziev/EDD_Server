from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from Tools import RES_SUCCESS, RES_BAD_REQUEST, is_user_valid
from user.models import Participant
from . import models
import datetime

# region Constants
EMA_HOURS = [10, 14, 18, 22]  # expected hours for ema responses
NUMBER_OF_EMA = len(EMA_HOURS)


# endregion

@csrf_exempt
@require_http_methods(['POST'])
def submit_api(request):
    req_body = request.body.decode('utf-8')
    json_body = json.loads(req_body)
    if 'username' in json_body and \
            'password' in json_body and \
            'ema_timestamp' in json_body and \
            'ema_order' in json_body and \
            'mood' in json_body and \
            'food' in json_body and \
            'physical_activity' in json_body and \
            'social_activity' in json_body and \
            'stress' in json_body and \
            'sleep_hour' in json_body and \
            'sleep_minute' in json_body and \
            is_user_valid(json_body['username'], json_body['password']):

        username = json_body['username']
        ema_timestamp = json_body['ema_timestamp']
        ema_order = json_body['ema_order']
        mood = json_body['mood']
        food = json_body['food']
        physical_activity = json_body['physical_activity']
        social_activity = json_body['social_activity']
        stress = json_body['stress']
        sleep_hour = json_body['sleep_hour']
        sleep_minute = json_body['sleep_minute']

        participant = Participant.objects.get(id=username)

        ema_datetime = datetime.datetime.fromtimestamp(ema_timestamp / 1000)
        ema_datetime_tmp = datetime.datetime(ema_datetime.year, ema_datetime.month, ema_datetime.day)
        reg_datetime = datetime.datetime.fromtimestamp(participant.register_datetime)
        reg_datetime_tmp = datetime.datetime(reg_datetime.year, reg_datetime.month, reg_datetime.day)
        current_day_num = (ema_datetime_tmp - reg_datetime_tmp).days + 1

        current_ema_row = models.Response.objects.all().get(username__id=username, day_num=current_day_num, ema_order=ema_order)

        current_ema_row.time_responded = ema_timestamp / 1000
        current_ema_row.mood = mood
        current_ema_row.food = food
        current_ema_row.physical_activity = physical_activity
        current_ema_row.social_activity = social_activity
        current_ema_row.stress = stress
        current_ema_row.sleep_hour = sleep_hour
        current_ema_row.sleep_minute = sleep_minute

        current_ema_row.save()

        return JsonResponse(data={'result': RES_SUCCESS})

    else:
        return JsonResponse(data={'result': RES_BAD_REQUEST})
