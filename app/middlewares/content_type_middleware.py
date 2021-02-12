from werkzeug.wrappers import Request, Response
from ..utils import response
import json


class ContentTypeMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        headers = request.headers

        if 'Content-Type' in headers:
            if 'application/json' in headers['Content-Type']:
                return self.app(environ, start_response)

        result = json.dumps({'result': 'requests must contain content-type application/json'})
        res = Response(result, content_type='application/json; charset=utf-8')
        res.status_code = 403

        return res(environ, start_response)
