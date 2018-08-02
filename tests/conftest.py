"""
    测试配置文件， 用于分享测试数据
"""

import os
import pytest
from flask import Flask as _Flask


class Flask(_Flask):
    testing = True
    secret_key = 'test key'


@pytest.fixture
def app():
    app = Flask('flask_test', root_path=os.path.dirname(__file__))
    return app


@pytest.fixture
def client(app):
    return app.test_client()