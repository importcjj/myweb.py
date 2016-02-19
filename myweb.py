# -*- coding: utf-8 -*-


from gevent.pywsgi import WSGIServer
from gevent import local
import functools
import types
from pprint import pprint

request = local.local()


class HttpCode(object):

    NOT_FOUND = '404 Not Found'
    OK = '200 OK'

http = HttpCode

request_fields = [
    ('PATH_INFO', 'url'),
    ('QUERY_STRING', 'params'),
    ('REMOTE_ADDR', 'remote_addr'),
    ('REMOTE_PORT', 'remote_port'),
    ('REQUEST_METHOD', 'method'),
    ('HTTP_USER_AGENT', 'agent')

]


class MyWebPy(object):

    def __init__(self, app_name, headers=None):
        """
        Useage:

        app = MyWebPy(__name,[
            ('Content-Type', 'text/html')
        ])

        """
        self.name = app_name
        # route map
        self.path_map = {}
        # Resonse Headers
        if not isinstance(headers, (list, types.NoneType)):
            raise ValueError('headers should be list type!')
        self.headers = headers if headers else []

    def application(self, env, start_response):
        # TODO: support more code
        self.set_request(env)
        if self.debug:
            pprint(env)
        handler = self.path_map.get(request.url, None)
        if not handler:
            start_response(http.NOT_FOUND, self.headers)
            return http.NOT_FOUND
        start_response(http.OK, self.headers)
        return handler()

    def start(self, host='127.0.0.1', port=7777, debug=False):
        """
        Useage:

        appinstance.start(host='127.0.0.1', port='7777')

        """
        self.debug = debug
        print('Serving on 7777...')
        WSGIServer((host, port), self.application).serve_forever()

    def route(self, path_info):
        """
        Useage:

        @appinstance.route('/index):
        def index():
            return 'This is the index'

        """
        def decorator(func):
            if path_info not in self.path_map:
                self.path_map[path_info] = func

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def set_request(self, wsgi_environ):
        """rewrite the request info in wsgi environ to the greenlet local variable `request`.

        method = request.method

        the mapping relationships is in request_fields.
        """
        for (r, f) in request_fields:
            setattr(request, f, wsgi_environ.get(r, None))

    def __str__(self):
        return '<MyWebPy.Application %s>' % self.name

if __name__ == '__main__':
    app = MyWebPy(__name__)

    @app.route('/')
    @app.route('/index')
    def index():
        return '%s %s ...' % (request.method, request.url)
    app.start()
