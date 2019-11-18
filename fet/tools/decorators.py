# coding=utf-8
import hashlib
from functools import wraps

from flask import current_app
from flask import jsonify
from flask import request


InvalidSignature = 'InvalidSignature'
ServerError = 'ServerError'
InvalidIPAddress = 'InvalidIPAddress'
NotFoundAuthApp = 'NotFoundAuthApp'


def get_ip():
    return request.headers.get("X-Forwarded-For") or request.remote_addr

def ip_required(white_list=None):
    """ ip限制"""
    if white_list is None:
        white_list = []
    elif not isinstance(white_list, list):
        white_list = [white_list]

    def deco(func):
        @wraps(func)
        def _deco(*args, **kw):
            default_white_list = current_app.config.get('WHITE_LIST')
            white_list.extend(default_white_list)
            ip = get_ip()
            if ip not in white_list:
                return jsonify(status=-1, message=InvalidIPAddress)
            return func(*args, **kw)
        return _deco
    return deco


def make_signature(app, secret, timestamp):
    """ 生成签名"""
    data = [app, str(timestamp), secret]
    return hashlib.md5('|'.join(data)).hexdigest()


def sign_required(func):
    """ 接口签名验证"""

    @wraps(func)
    def deco(*args, **kw):
        auth_apps = current_app.config.get('AUTH_APPS') or {}
        if not auth_apps:
            return jsonify(status=-1, message=NotFoundAuthApp)

        params = request.args.to_dict()
        try:
            app, t, sig = params['_app'], params['_t'], params['_sig']
        except KeyError:
            return jsonify(status=-1, message=InvalidSignature)

        if app not in auth_apps:
            return jsonify(status=-1, message=InvalidSignature)

        signature = make_signature(app, auth_apps[app], t)
        if sig != signature:
            return jsonify(status=-1, message=InvalidSignature)

        return func(*args, **kw)
    return deco
