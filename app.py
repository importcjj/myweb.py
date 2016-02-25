# -*- coding: utf-8 -*-

from myweb import (
    MyWebPy,
    Proxy
)


proxy = Proxy()
app = MyWebPy(__name__, proxy=proxy)


@app.route('/')
@app.route('/index')
def index():
    return "hello world"


@app.proxy.get('*')
def handler(response):
    response._content = '''<h1 style="text-align:center">Proxy<h1>'''
    return response

app.start()
