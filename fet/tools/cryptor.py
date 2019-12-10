import base64
import functools
from binascii import a2b_hex
from binascii import b2a_hex

from Crypto.Cipher import AES

from fet.utils import to_bytes
from fet.utils import to_string


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


class _AES(object):

    def __init__(self, key, iv, mod=AES.MODE_CBC):
        self.key = to_bytes(key[:16])
        self.iv = to_bytes(iv)
        self.mod = mod

    def __pad(self, text):
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        return text + bytes([amount_to_pad]) * amount_to_pad

    def __unpad(self, text):
        pad = ord(text[-1])
        return text[:-pad]

    def encrypt(self, raw):
        """加密"""
        raw = to_bytes(raw)
        raw = self.__pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(raw))

    def decrypt(self, enc):
        """解密"""
        enc = to_bytes(enc)
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return self.__unpad(to_string(cipher.decrypt(enc)))
