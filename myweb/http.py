# -*- coding: utf-8 -*-

import requests
from requests.api import request

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

        :param wsgi_env: (dict). From gevent wsgi server.
        """
        self.headers = {HEADERS[h1]: h2 for h1,
                        h2 in env.items() if HEADERS.get(h1)}
        self.method = env['REQUEST_METHOD']
        self.scheme = env['wsgi.url_scheme']
        self.host = env['HTTP_HOST']
        self.path = env['PATH_INFO']
        if self.host not in self.path:
            self.url = self.host + self.path
        else:
            self.url = self.path
        self.data = env['wsgi.input'].read()
        self.params = env['QUERY_STRING']

        self.allow_redirects = False

    def send(self, **kwargs):
        """Send a Request."""
        try:
            resp = request(self.method, self.url,
                           headers=self.headers,
                           params=self.params,
                           data=self.data,
                           allow_redirects=self.allow_redirects,
                           **kwargs)
        except requests.RequestException as ex:
            raise ex
        return Response(resp)


DROP_HEADERS = ['Content-Encoding', 'Transfer-Encoding']


class Response(object):

    def __init__(self, response):
        """Response object for myweb.

        :param response: (requests.Response). Response of requests.
        """
        self._headers = response.headers
        for header in DROP_HEADERS:
            self._headers.pop(header, None)
        self.content = response.content
        self.status_code = response.status_code

    @property
    def headers(self):
        """Get Headers."""
        self._headers['Content-Length'] = len(self.content)
        return [(k, v) for k, v in self._headers.items() if k]

    @headers.setter
    def headers(self, h):
        """Set Headers.

        :param h: (dict). New headers dict.

        .. warning::
            some header key-value will be droped.
        """
        self._headers = {k: v for k, v in h.items() if k not in DROP_HEADERS}
