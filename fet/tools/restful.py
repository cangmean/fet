# coding=utf-8
import flask_restful
from flask import abort
from flask import Blueprint
from flask import jsonify
from flask.views import MethodView
from flask_restful.reqparse import Argument
from flask_restful.reqparse import RequestParser
from fet.utils import to_string



class ApiJsonify(object):
    @classmethod
    def response(cls, code, errmsg="", **kw):
        dic = {"code": code, "errmsg": errmsg, "data": kw}
        return jsonify(**dic)

    @classmethod
    def ok(cls, **kw):
        return cls.response('0', **kw)

    @classmethod
    def no(cls, errmsg, code='-1', **kw):
        return cls.response(code, errmsg=errmsg, **kw)


api_jsonify = ApiJsonify()


def _abort(http_status_code, *args, **kw):
    errmsg = kw['message'].values()[0]
    response = api_jsonify.no(errmsg, code=http_status_code)
    response.headers['Content-Type'] = 'application/json'
    abort(response)


flask_restful.abort = _abort


class RestApi(object):
    def __init__(self, name, import_name, **kw):
        self.bp = Blueprint(name, import_name, **kw)

    def route(self, url, **options):
        """ 通过装饰器注册路由

        以下是例子:

            api = RestApi('home', __name__)

            @api.route('/')
            @api.route('/home, endpoint='home')
            class HomeApi(RestView):

                def get(self):

                    return self.ok()

        也可以限制每个路由接受的方法

            @api.route('/', methods=['GET'])
            @api.route('/create, methods=['POST'])
            class EmployeeCreateApi(RestView):

                def get(self):
                    return self.ok()

                def post(self):
                    name = request.form.get('name')
                    ...
                    return self.ok()

        """

        def decorator(cls):
            endpoint = options.pop("endpoint", None) or cls.__name__
            methods = options.pop("methods", None) or cls.methods
            self.bp.add_url_rule(
                url, view_func=cls.as_view(endpoint), methods=methods)
            return cls
        return decorator

    def before_app_request(self, func):
        return self.bp.before_app_request(func)


class RestView(MethodView, ApiJsonify):
    """ 视图类"""

    @classmethod
    def set_model_fields(cls, obj, fields, excludes=[]):
        """ 设置模型的字段"""
        for field, value in fields.items():
            if hasattr(obj, field) and field not in excludes:
                if value or value == 0:
                    setattr(obj, field, value)


class _Argument(Argument):

    def __init__(self, name, **kw):
        self.validators = kw.pop('validators', None)
        kw['dest'] = kw.pop('rename', None)
        kw['help'] = kw.pop('message', None)

        Argument.__init__(self, name, **kw)
        self.parse = self.process_parse(self.parse)

    def validate(self, value):
        """ 验证"""
        validators = self.validators or []
        for validator in validators:
            if callable(validator):
                try:
                    validator(value)
                except Exception as error:
                    error_message = getattr(validator, 'message', '') or to_string(error)
                    _abort('-1', message={self.name: error_message})

    def process_parse(self, func):
        """ 装饰解析的值"""
        def deco(*args, **kw):
            results, _found = func(*args, **kw)
            if not isinstance(results, ValueError):
                self.validate(results)
            return results, _found
        return deco


class Parser(RequestParser):

    def __init__(self, **kw):
        if 'argument_class' not in kw:
            kw['argument_class'] = _Argument
        RequestParser.__init__(self, **kw)

    def add(self, field_name, **kw):
        self.add_argument(field_name, **kw)

    def get_values(self):
        data = self.parse_args()
        return data
