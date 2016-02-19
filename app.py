# -*- coding: utf-8 -*-

from myweb import (
    MyWebPy,
    request
)


app = MyWebPy(__name__)


@app.route('/')
@app.route('/index')
def index():
    path = request.url
    method = request.method
    return "%s %s " % (method, path)

app.start()
