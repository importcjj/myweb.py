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
def handler(request, response):
    return response

app.start()
