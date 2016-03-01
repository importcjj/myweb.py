# -*- coding: utf-8 -*-

from myweb import (
    MyWebPy,
    Proxy
)
import re


proxy = Proxy()
app = MyWebPy(__name__, proxy=proxy)


re_body_ = re.compile(r'\<body.*?\>(.+?)</body>', re.S)

nav_style = {
    'position': 'fixed',
    'z-index': '99999',
    'background': '#ccc',
    'width': '100%',
    'height': '50px',
    'top': '0px',
    'left': '0px',
    'box-sizing': 'border-box',
    'border-right': '1px solid #ccc'
}

body_box_style = {
    'margin-top': '50px'
}


def stylefmt(style):
    return ';'.join([':'.join([k, v]) for k, v in style.items()])

import os.path

html_dir = os.path.realpath('../examples')
insert = r"""
    <iframe style="%s" src="file:///Users/eleme/Personal/chrome/popup.html" seamless></iframe>
    <div style="%s"> \1 <div>
""" % (stylefmt(nav_style), stylefmt(body_box_style))


from pprint import pprint


@app.proxy.post()
def post_handler(request, response):
    print 'Request Data'.ljust(60, '=')
    pprint(request.data)
    print 'Request Headers'.ljust(60, '=')
    pprint(request.headers)
    print 'Response Headers'.ljust(60, '=')
    print response.headers
    print 'Response Cookies'.ljust(60, '=')
    print response.cookies

    cookies = response.cookies
    print cookies
    return response


@app.proxy.get(host='python.freelycode.com')
def get_handler(request, response):
    print request.headers
    return response

app.start()
