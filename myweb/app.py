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
    'width': '70px',
    'height': '100%',
    'box-sizing': 'border-box',
    'border-right': '1px solid #ccc'
}

body_box_style = {
    'margin-left': '70px'
}


def stylefmt(style):
    return ';'.join([':'.join([k, v]) for k, v in style.items()])

insert = r"""
    <div style="%s">Proxy Docker</div>
    <div style="%s"> \1 <div>
""" % (stylefmt(nav_style), stylefmt(body_box_style))


@app.proxy.get()
def handler(request, response):
    if 'text/html' in response._headers['Content-Type']:
        response.content, count = re_body_.subn(
            insert, response.content)
    return response

app.start()
