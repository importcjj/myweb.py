# -*- coding: utf-8 -*-

import requests
from requests.api import request
import httplib

HEADERS = {
    'HTTP_ACCEPT': 'Accept',
    'HTTP_ACCEPT_ENCODING': 'Accept-Encoding',
    'HTTP_ACCEPT_LANGUAGE': 'Accept-Language',
    'HTTP_CACHE_CONTROL': 'Cache-Control',
    'HTTP_CONNECTION': 'Connection',
    'HTTP_HOST': 'Host',
    'HTTP_DNT': 'DNT',
    'HTTP_USER_AGENT': 'User-Agent',
}


class Request(object):

    def __init__(self, env):
        """Request object for myweb.

        :param wsgi_env(dict): from gevent wsgi server.
        """
        self.headers = {h2: env[h1]for h1, h2 in HEADERS.items()}
        self.method = env['REQUEST_METHOD']
        self.scheme = env['wsgi.url_scheme']
        self.host = env['HTTP_HOST']
        self.path = env['PATH_INFO']
        self.url = self.host + self.path
        self._input = env['wsgi.input']
        self.params = env['QUERY_STRING']

    @property
    def data(self):
        return self._input.read()

    def done(self, **kwargs):
        """Send a Request."""
        try:
            resp = request(self.method, self.url,
                           headers=self.headers,
                           params=self.params,
                           data=self.data,
                           **kwargs)
        except requests.RequestException as ex:
            raise httplib.HTTPException(ex.response)
        return Response(resp)


DROP_HEADERS = ['Content-Encoding']


class Response(object):

    def __init__(self, Response):
        """Response object for myweb.

        :param response(requests.Response): response of requests.
        """
        self._headers = Response.headers
        self.content = Response.content
        self.status_code = Response.status_code

    @property
    def headers(self):
        """Get Headers."""
        self._headers['Content-Length'] = len(self.content)
        return self._headers

    @headers.setter
    def headers(self, h):
        """Set Headers.

        :param h(dict): new headers dict.

        .. warning::
            some header key-value will be droped.
        """
        self._headers = {k: v for k, v in h.items() if k not in DROP_HEADERS}
