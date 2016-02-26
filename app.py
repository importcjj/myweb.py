# -*- coding: utf-8 -*-

from myweb import (
    MyWebPy,
    Proxy
)

import time


proxy = Proxy()
app = MyWebPy(__name__, proxy=proxy)


@app.route('/')
@app.route('/index')
def index():
    return "hello world"


@app.proxy.get(host='runoob.com')
def handler(request, response):
    time.sleep(20)
    return response

app.start()
