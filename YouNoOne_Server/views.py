from Tools import extract_post_params, RES_FAILURE, RES_SUCCESS, RES_BAD_REQUEST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import subprocess

from user.views import is_user_valid


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
