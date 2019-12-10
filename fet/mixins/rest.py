# coding=utf-8
from flask import jsonify


class RestError(object):

    NF = NotFound = "NotFound"
    AE = AlreadyExists = "AlreadyExists"
    UA = InvalidUsernameOrPassword = "InvalidUsernameOrPassword"


class ApiJsonify(RestError):

    @classmethod
    def response(cls, code, errmsg="", **kw):
        dic = {"code": code, "errmsg": errmsg, "data": kw}
        return jsonify(**dic)

    @classmethod
    def ok(cls, code=200, **kw):
        return cls.response(code, **kw)

    @classmethod
    def no(cls, errmsg, code=500, **kw):
        return cls.response(code, errmsg=errmsg, **kw)
