import time
from werkzeug import serving
from werkzeug._internal import _log
from flask import Flask
from fet.utils import get_current_time

__all__ = ['_Flask', '__version__']

__version__ = '0.1'


class _FetRequestHandler(serving.WSGIRequestHandler):

    def handle_one_request(self):
        """ 重写父类方法"""
        self._st = time.time()
        return super().handle_one_request()

    def send_response(self, code, message=None):
        """ 重写父类方法"""
        self._et = time.time()
        return super().send_response(code, message=None)

    def get_rtime(self):
        """ 响应耗时"""
        rtime = (self._et - self._st) * 1000
        rtime = round(rtime, 2)
        return rtime

    def log(self, type, message, *args):
        rtime = self.get_rtime()
        rtime_message = 'rtime = %s ms' % rtime
        message = message % (args[0], args[1], rtime_message)
        message = '[%s] [%s] %s' % (type.upper(), get_current_time(), message)
        _log(type, message)


class _Flask(Flask):
    """ Flask子类， 用于重写默认werkzeug打印的日志

        from fet import _Flask as Flask

        app = Flask(__name__)
        ...
        app.run()

    """

    def run(self, host=None, port=None, debug=None,
            load_dotenv=True, **options):

        options.setdefault('request_handler', _FetRequestHandler)
        super().run(
            host, port, debug, load_dotenv, **options
        )
