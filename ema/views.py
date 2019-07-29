from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from user.models import Participant
from user.views import RES_SUCCESS, RES_BAD_REQUEST
from . import models
import datetime


# Create your views here.
def user_exists(username):
    return Participant.objects.filter(username=username).exists()


def is_user_valid(username, password):
    if user_exists(username):
        participant = Participant.objects.get(username=username)
        return participant.password == password
    return False


@csrf_exempt
@require_http_methods(['POST'])
def submit_api(request):
    req_body = request.body.decode('utf-8')
    json_body = json.loads(req_body)
    if 'username' in json_body and \
            'password' in json_body and \
            'ema_timestamp' in json_body and \
            'ema_order' in json_body and \
            'ema_responses' in json_body and \
            is_user_valid(json_body['username'], json_body['password']):

        username = json_body['username']
        ema_timestamp = json_body['ema_timestamp']
        ema_order = json_body['ema_order']
        ema_responses = json_body['ema_responses']

        participant = Participant.objects.get(username=username)

        ema_datetime = datetime.datetime.fromtimestamp(ema_timestamp / 1000)
        ema_datetime_tmp = datetime.datetime(ema_datetime.year, ema_datetime.month, ema_datetime.day)
        reg_datetime = datetime.datetime.fromtimestamp(participant.register_datetime)
        reg_datetime_tmp = datetime.datetime(reg_datetime.year, reg_datetime.month, reg_datetime.day)
        current_day_num = (ema_datetime_tmp - reg_datetime_tmp).days + 1

        current_ema_row = models.Response.objects.all().get(username__username=username, day_num=current_day_num)

        if ema_order == 1:
            current_ema_row.ema_1 = ema_responses
        elif ema_order == 2:
            current_ema_row.ema_2 = ema_responses
        elif ema_order == 3:
            current_ema_row.ema_3 = ema_responses
        elif ema_order == 4:
            current_ema_row.ema_4 = ema_responses
        elif ema_order == 5:
            current_ema_row.ema_5 = ema_responses
        elif ema_order == 6:
            current_ema_row.ema_6 = ema_responses

        current_ema_row.save()
        return JsonResponse(data={'result': RES_SUCCESS})

    else:
        return JsonResponse(data={'result': RES_BAD_REQUEST})
