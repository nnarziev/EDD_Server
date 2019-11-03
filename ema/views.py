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
            'answers' in json_body and \
            is_user_valid(json_body['username'], json_body['password']):

        username = json_body['username']
        ema_timestamp = json_body['ema_timestamp']
        ema_order = json_body['ema_order']
        interest, mood, sleep, fatigue, weight, worthlessness, concentrate, restlessness, suicide = json_body['answers'].split(" ")

        participant = Participant.objects.get(id=username)

        ema_datetime = datetime.datetime.fromtimestamp(ema_timestamp / 1000)
        ema_datetime_tmp = datetime.datetime(ema_datetime.year, ema_datetime.month, ema_datetime.day)
        reg_datetime = datetime.datetime.fromtimestamp(participant.register_datetime)
        reg_datetime_tmp = datetime.datetime(reg_datetime.year, reg_datetime.month, reg_datetime.day)
        current_day_num = (ema_datetime_tmp - reg_datetime_tmp).days + 1

        current_ema_row = models.Response.objects.all().get(username__id=username, day_num=current_day_num, ema_order=ema_order)

        current_ema_row.time_responded = ema_timestamp / 1000

        current_ema_row.interest = interest
        current_ema_row.mood = mood
        current_ema_row.sleep = sleep
        current_ema_row.fatigue = fatigue
        current_ema_row.weight = weight
        current_ema_row.worthlessness = worthlessness
        current_ema_row.concentrate = concentrate
        current_ema_row.restlessness = restlessness
        current_ema_row.suicide = suicide

        current_ema_row.save()

        return JsonResponse(data={'result': RES_SUCCESS})

    else:
        return JsonResponse(data={'result': RES_BAD_REQUEST})
