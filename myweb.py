# -*- coding: utf-8 -*-


from gevent.pywsgi import WSGIServer
from gevent import local
import functools
import types
import httplib
import requests
from collections import defaultdict
import urlparse
from pprint import pprint

request = local.local()


class HttpCode(object):

    NOT_FOUND = '404 Not Found'
    OK = '200 OK'

http = HttpCode

request_fields = [
    ('PATH_INFO', 'url'),
    ('HTTP_HOST', 'host'),
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
        # proxy
        self.proxy = None
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
        if self.proxy and request.host != ':'.join([self.host, self.port]):
            return self.proxy(request.url, start_response, None)
        handler = self.path_map.get(request.url, None)
        if not handler:
            start_response(http.NOT_FOUND, self.headers)
            return http.NOT_FOUND
        start_response(http.OK, self.headers)
        return handler()

    def start(self, host='127.0.0.1', port=7777, debug=False, proxy=None):
        """
        Useage:

        appinstance.start(host='127.0.0.1', port='7777')

        """
        self.host = host
        self.port = port
        self.debug = debug
        self.proxy = proxy
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
        print wsgi_environ['wsgi.input'].read()
        for (r, f) in request_fields:
            setattr(request, f, wsgi_environ.get(r, None))

    def __str__(self):
        return '<MyWebPy.Application %s>' % self.name


class Proxy(object):

    methods = {
        'GET': 'do_get',
        'POST': 'do_post',
        'PUT': 'do_put',
        'PATCH': 'do_patch',
        'DELETE': 'do_delete'
    }

    headers = []

    def __init__(self, headers=None):
        if headers:
            self.headers = headers
        self.middleware = {
            '*': ProxyMiddleware('common')
        }

    def __call__(self, path, start_response, proxy_url):
        if '://' not in path:
            path = 'http://' + path

        method = request.method
        do_method = self.methods[method]
        if not do_method:
            raise httplib.METHOD_NOT_ALLOWED
        return do_method(path, start_response, proxy_url)

    def do_get(self, path, start_response, proxy_url):
        return requests.get(path)

    def do_post(self, path, start_response, proxy_url):
        pass

    def do_patch(self, path, start_response, proxy_url):
        pass

    def do_put(self, path, start_response, proxy_url):
        pass

    def do_delete(self, path, start_response, proxy_url):
        pass

    def _decorator(self, method, func, host=None):
        @functools.wraps(func)
        def wrapper(response, *args, **kwargs):
            if method == 'GET':
                pass

    def get(self, host=None):
        return NotImplementedError

    def post(self, path, start_response, proxy_url):
        raise NotImplementedError

    def patch(self, path, start_response, proxy_url):
        raise NotImplementedError

    def put(self, path, start_response, proxy_url):
        raise NotImplementedError


class ProxyMiddleware(object):

    methods = ['get', 'post', 'put', 'patch', 'delete']

    def __init__(self, name, host='*'):
        self.name = name
        self.host = host
        self.handles = defaultdict(list)

    def add_handler(self, method, handler):
        self.method.append(handler)

    def __getattr__(self, k):
        if k in self.methods:
            return self.handles[k]
        return self.__dict__.get(k)

if __name__ == '__main__':
    proxy = Proxy()
    app = MyWebPy(__name__)

    @app.route('/')
    @app.route('/index')
    def index():
        return '%s %s ...' % (request.method, request.url)
    app.start(debug=True)
