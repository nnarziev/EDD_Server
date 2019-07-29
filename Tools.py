import json


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



