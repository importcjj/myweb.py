========
myweb.py
========
一个仿照flask的基于gevent的web玩具框架.


简单的代理功能(目前仅支持GET请求)


.. code-block:: python

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


    @app.proxy.get(host='*')
    def handler(response):
        response._content = '''<h1 style="text-align:center">Proxy<h1>'''
        return response

    app.start()

