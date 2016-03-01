# -*- coding: utf-8 -*-

import requests
import httplib
from requests.api import request
from Cookie import SimpleCookie


HEADERS = {
    'HTTP_ACCEPT': 'Accept',
    'HTTP_ACCEPT_ENCODING': 'Accept-Encoding',
    'HTTP_ACCEPT_LANGUAGE': 'Accept-Language',
    'HTTP_CACHE_CONTROL': 'Cache-Control',
    'HTTP_CONNECTION': 'Connection',
    'HTTP_HOST': 'Host',
    'HTTP_DNT': 'DNT',
    'HTTP_USER_AGENT': 'User-Agent',
    'HTTP_REFERER': 'Referer',
    'HTTP_ORIGIN': 'Origin',
    'CONTENT_TYPE': 'Content-Type',
    'CONTENT_LENGTH': 'Content-Length',
}


def parse_cookies(cookies_string):
    """"""
    cookies = {}
    if not cookies_string:
        return {}
    morsels = cookies_string.split(';')
    for morsel in morsels:
        c = morsel.strip().split('=')
        if c:
            cookies[c[0]] = c[1] if len(c) > 1 else ''
    return cookies


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
        self.cookies = parse_cookies(env.get('HTTP_COOKIE'))
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
                           cookies=self.cookies,
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
        self._status_code = httplib.OK
        self._headers = []
        self._cookies = []

        cookies_str = response.headers.pop('Set-Cookie', None)
        if cookies_str:
            self.cookies = cookies_str
        self.content = response.content
        self.headers = response.headers
        self.status_code = response.status_code


    @property
    def headers(self):
        """Get Headers

        """
        return self._headers

    @headers.setter
    def headers(self, h):
        """Set Headers.

        :param h: (dict). New headers dict.

        .. warning::
            Some header key-value will be droped,
            And if status code is 204, auto drop `Content-Length`.
            Default Content-Type is `text/html; charset=utf-8`.
        """
        self._headers = {k: v for k, v in h.items() if k not in DROP_HEADERS}

        self._headers['Content-Length'] = len(self.content)

        if not self._headers.get('Content-Type'):
            self._headers['Content-Type'] = 'text/html; charset=utf-8'

        if self._status_code == httplib.NO_CONTENT:
            self._headers.pop('Content-Length', None)

    @property
    def status_code(self):
        """Get Status Code

        """
        return self._status_code

    @status_code.setter
    def status_code(self, code):
        """Set Status Code.

        :param code: (int). New status code.

        .. warning::
            If the new status code equal to `httplib.NO_CONETNT`,
            auto drop the `Content-Length` in Headers.
        """
        if code == httplib.NO_CONTENT and self._headers.get('Content-Length'):
            del self._headers['Content-Length']

        self._status_code = code

    @property
    def cookies(self):
        """Get Response Cookies
        
        """
        return self._cookies

    @cookies.setter
    def cookies(self, rawdata):
        """Set Response Cookies.

        :param rawdata: (str or dict). List of `cookielib.Cookie`.
        """
        sc = SimpleCookie()
        sc.load(rawdata)
        self._cookies = sc.items()
    

    def wsgi_headers(self):
        """Get Headers list for start_response()

        example:

            [('Content-Length', '90'), ('Set-Cookie', 'name=myweb')]
        """
        h = [(k, v) for k, v in self._headers.items() if k]
        h.extend([('Set-Cookie', morsel.OutputString() )for name, morsel in self._cookies])
        return h
