import datetime


def to_bytes(text, fmt='utf8'):
    """ 转成bytes"""
    if isinstance(text, str):
        text = text.encode(fmt)
    return text


def to_string(text, fmt='utf8'):
    """ 转成string"""
    if isinstance(text, bytes):
        text = text.decode(fmt, 'ignore')
    return text


def get_current_time(fmt="%F %T"):
    """ 获取当前时间字符串"""
    return datetime.datetime.now().strftime(fmt)