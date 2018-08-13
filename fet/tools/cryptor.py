import functools
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from fet.utils import to_bytes, to_string


def wrap_encode(input_func=None, output_func=None):
    """
    :param input_func: 输入时候的字符编码
    :param output_func: 输出时候的字符编码
    :return: 编码后的密码
    """
    def wrap_func(func):
        @functools.wraps(func)
        def deco(app, *args, **kw):
            text = input_func(args[0]) if input_func else args[0]
            args = (text, ) + args[1:]
            ret = func(app, *args, **kw)
            ret = output_func(ret) if output_func else ret
            return ret
        return deco
    return wrap_func


class Cryptor(object):

    def __init__(self, app=None):
        self._SECRET_KEY = None
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        
        app.config.setdefault(
            'FET_AES_SECRET_KEY',
            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        )

        app.extensions['fet_cryptor'] = self
        if not self._SECRET_KEY:
            self._SECRET_KEY = to_bytes(app.config['FET_AES_SECRET_KEY'])
    
    @wrap_encode(input_func=to_bytes)
    def ensure_key(self, text):
        """ 有效的密钥"""
        length, count = 16, len(text)
        add = length - (count % length)
        text += b'\0' * add
        return text
    
    @wrap_encode(to_bytes, to_string)
    def encrypt(self, text, salt=None):
        """ 加密"""
        text = self.ensure_key(text)
        salt = self.ensure_key(salt) if salt else self._SECRET_KEY[:16]
        crypt = AES.new(self._SECRET_KEY[:16], AES.MODE_CBC, salt)
        plain_text = crypt.encrypt(text)
        return b2a_hex(plain_text)
    
    @wrap_encode(to_bytes, to_string)
    def decrypt(self, text, salt=None):
        """ 解密"""
        salt = self.ensure_key(salt) if salt else self._SECRET_KEY[:16]
        crypt = AES.new(self._SECRET_KEY[:16], AES.MODE_CBC, salt)
        plain_text = crypt.decrypt(a2b_hex(text))
        plain_text = plain_text.rstrip(b'\0')
        return plain_text