import json
from user import models

RES_SUCCESS = 0
RES_FAILURE = 1
RES_BAD_REQUEST = -1

def user_exists(username):
    return models.Participant.objects.filter(id=username).exists()


def is_user_valid(username, password):
    if user_exists(username):
        user = models.Participant.objects.get(id=username)
        return user.password == password
    return False


def extract_post_params(request):
    _files = request.FILES
    if 'username' in _files:
        return json.loads('{"username": "%s", "password": "%s"}' % (
            _files['username'].read().decode('utf-8'),
            _files['password'].read().decode('utf-8')
        ))
    _post = request.POST
    if 'username' in _post:
        return _post
    else:
        return json.loads(request.body.decode('utf-8'))
