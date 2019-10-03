from Tools import extract_post_params
from user.views import RES_SUCCESS, RES_BAD_REQUEST, RES_FAILURE
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from user.models import Participant
from ema.models import Response
import json
import subprocess


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


@csrf_exempt
@require_http_methods(['POST'])
def submit_audio(request):
    try:
        params = extract_post_params(request)
        if 'username' not in params or 'password' not in params or 'file' not in request.FILES:
            raise ValueError('username/password/file is not in request params')
        if not is_user_valid(params['username'], params['password']):
            return JsonResponse({'result': RES_FAILURE})
        else:
            username = params['username']
            audio_file = request.FILES['file']
            timestamp = audio_file.name[:audio_file.name.index('.')]
            audio_data = audio_file.read()

            with open('audio/%s_%s.mp4' % (username, timestamp), 'wb') as w:
                w.write(audio_data)

            convert_command = 'C:\\ffmpeg\\bin\\ffmpeg.exe -i audio/%s_%s.mp4 -ab 160k -ac 2 -ar 44100 -vn audio/%s_%s.wav' % (username, timestamp, username, timestamp)
            subprocess.call(convert_command, shell=True)
            return JsonResponse(data={'result': RES_SUCCESS})
    except ValueError as e:
        print(e)
        return JsonResponse({'result': RES_BAD_REQUEST})
