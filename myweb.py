# -*- coding: utf-8 -*-

from __future__ import absolute_import
from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer
from gevent import local
import functools
import types
import httplib
from collections import defaultdict
from functools import partial
from urlparse import urlparse
from pprint import pprint
import requests as grequests
import urllib
from http_code import http_status as status_code

urllib.getproxies_environment = lambda: {'_': '_'}

request = local.local()
HTTP_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'CONNECT']


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
        # TODO: support more code
        self.set_request(env)
        if self.debug:
            pprint(env)
        start_response(status_code.NOT_FOUND, self.headers)
        if self.proxy and request.host != self.hostname:
            return self.proxy(request.url, start_response, None)
        handler = self.path_map.get(request.url, None)
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

    def set_request(self, wsgi_environ):
        """rewrite the request info in wsgi environ to the greenlet local variable `request`.

        method = request.method

        the mapping relationships is in request_fields.
        """
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
        'DELETE': 'do_delete',
        'CONNECT': 'do_connect'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }
    drop_headers = ['Transfer-Encoding', 'Set-Cookie', 'Content-Encoding', 'Content-Length']

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
        return getattr(self, do_method)(path, start_response, proxy_url)

    def do_get(self, path, start_response, proxy_url):
        response = grequests.get(path, headers=self.headers)
        headers = [(k, v) for k, v in response.headers.items() if k not in self.drop_headers]
        host = urlparse(path).hostname

        response = self.middleware['*'].handle(response)
        for k, v in self.middleware.items():
            if k in host:
                response = v.handle(response)
        start_response(status_code[response.status_code], headers)
        return [response.content]

    def do_post(self, path, start_response, proxy):
        return 'Not Allowed.'

    def do_patch(self, path, start_response, proxy):
        return 'Not Allowed'

    def do_put(self, path, start_response, proxy):
        return 'Not Allowed.'

    def do_delete(self, path, start_response, proxy):
        return 'Not Allowed.'

    def do_connect(self, path, start_response, proxy):
        return 'Not Allowed.'

    def register_handler(self, method, host='*'):
        def _decorator(func):
            if host not in self.middleware:
                self.middleware[host] = ProxyMiddleware(name=host, host=host)
            getattr(self.middleware[host], method).append(func)

            @functools.wraps(func)
            def wrapper(response, *args, **kwargs):
                return func(response, *args, **kwargs)
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

    def handle(self, response):
        method = request.method
        if method not in self.methods:
            raise httplib.METHOD_NOT_ALLOWED
        for handler in self.handlers[method]:
            response = handler(response)
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
        return '%s %s ...' % (request.method, request.url)
    app.start(debug=True)
