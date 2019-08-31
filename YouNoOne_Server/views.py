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
        current_day_num = participant.current_day_num()
        ema_responses = Response.objects.filter(username=participant, day_num=current_day_num).order_by('time_expected')
        data = []
        for ema in ema_responses:
            data += [ema.mood]
        return JsonResponse(data={'result': RES_SUCCESS, 'data': data})
    else:
        return JsonResponse(data={'result': RES_BAD_REQUEST})
