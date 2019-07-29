from user.views import RES_SUCCESS, RES_BAD_REQUEST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from user.models import Participant
from ema.models import Response
import datetime
import json


def user_exists(username):
    return Participant.objects.filter(username=username).exists()


def is_user_valid(username, password):
    if user_exists(username):
        participant = Participant.objects.get(username=username)
        return participant.password == password
    return False


@csrf_exempt
@require_http_methods(['POST'])
def fetch_mood_data(request):
    req_body = request.body.decode('utf-8')
    json_body = json.loads(req_body)
    if 'username' in json_body and 'password' and is_user_valid(json_body['username'], json_body['password']):
        username = json_body['username']
        participant = Participant.objects.get(username=username)
        cur_day = (datetime.datetime.now() - datetime.datetime.fromtimestamp(participant.register_datetime)).days + 1
        ema_responses = Response.objects.filter(username=participant, day_num=cur_day)
        tmp_data = []
        for ema in ema_responses:
            tmp_data += [ema.ema_1.split(',')[0], ema.ema_2.split(',')[0], ema.ema_3.split(',')[0], ema.ema_4.split(',')[0], ema.ema_5.split(',')[0], ema.ema_6.split(',')[0]]
        data = [int(elem) if elem != '-' else 0 for elem in tmp_data]
        return JsonResponse(data={'result': RES_SUCCESS, 'data': data})
    else:
        return JsonResponse(data={'result': RES_BAD_REQUEST})
