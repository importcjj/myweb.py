# -*- coding: utf-8 -*-

from __future__ import absolute_import
from gevent import monkey
monkey.patch_all()  # noqa
from gevent import local
from gevent.pywsgi import WSGIServer

import urllib
import functools
import types
from collections import defaultdict
from functools import partial
from .http_code import http_status as status_code
from .http import Request


urllib.getproxies_environment = lambda: {'_': '_'}

this = local.local()
HTTP_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'CONNECT']


class MyWebPy(object):

    def __init__(self, app_name, headers=None, proxy=None):
        """
        Useage:

        app = MyWebPy(__name,[
            ('Content-Type', 'text/html')
        ])

        """
        self.name = app_name
        # proxy
        self.proxy = proxy
        # route map
        self.path_map = {}
        # Resonse Headers
        if not isinstance(headers, (list, types.NoneType)):
            raise ValueError('headers should be list type!')
        self.headers = headers if headers else []

    def application(self, env, start_response):
        this.request = Request(env)
        if self.proxy and this.request.host != self.hostname:
            resp = self.proxy(this.request)
            start_response(status_code[resp.status_code], resp.wsgi_headers())
            return [resp.content]

        handler = self.path_map.get(this.request.path, None)
        if not handler:
            start_response(status_code.NOT_FOUND, self.headers)
            return status_code.NOT_FOUND

        start_response(status_code.OK, self.headers)
        return handler()

    def start(self, host='127.0.0.1', port=7777, debug=False):
        """
        Useage:

        appinstance.start(host='127.0.0.1', port=7777)

        """
        self.host = host
        self.port = port
        self.hostname = ':'.join([host, str(port)])
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

    def __str__(self):
        return '<MyWebPy.Application %s>' % self.name


class Proxy(object):

    methods = HTTP_METHODS

    def __init__(self):
        self.middleware = {
            '*': ProxyMiddleware('common')
        }

    def __call__(self, request):
        if '://' not in request.url:
            request.url = 'http://' + request.url

        return self.handle(request)

    def handle(self, request):
        response = request.send()
        response = self.middleware['*'].handle(request, response)
        for k, v in self.middleware.items():
            if k in request.host:
                response = v.handle(request, response)
        return response

    def register_handler(self, method, host='*'):
        def _decorator(func):
            if host not in self.middleware:
                self.middleware[host] = ProxyMiddleware(name=host, host=host)
            getattr(self.middleware[host], method).append(func)

            @functools.wraps(func)
            def wrapper(request, response, *args, **kwargs):
                return func(request, response, *args, **kwargs)
            return wrapper
        return _decorator

    def __getattr__(self, k):
        if k.upper() in self.methods:
            return partial(self.register_handler, k.upper())
        return self.__dict__[k]


class ProxyMiddleware(object):

    methods = HTTP_METHODS

    def __init__(self, name, host='*'):
        self.name = name
        self.host = host
        self.handlers = defaultdict(list)

    def add_handler(self, method, handler):
        self.method.append(handler)

    def handle(self, request, response):
        for handler in self.handlers[request.method]:
            response = handler(request, response)
        return response

    def __getattr__(self, k):
        if k.upper() in self.methods:
            return self.handlers[k]
        return self.__dict__.get(k)

if __name__ == '__main__':
    proxy = Proxy()
    app = MyWebPy(__name__)

    @app.route('/')
    @app.route('/index')
    def index():
        return '%s %s ...' % (this.request.method, this.request.url)
    app.start(debug=True)
