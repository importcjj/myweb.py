# -*- coding: utf-8 -*-

from myweb import (
    MyWebPy,
    request
)
import time

app = MyWebPy(__name__)


@app.route('/')
@app.route('/index')
def index():
    for i in xrange(9):
        yield str(i)

app.start()
