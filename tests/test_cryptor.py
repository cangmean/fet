from fet.tools.cryptor import Cryptor


def test_cryptor(app):
    cryptor = Cryptor(app)
    x = cryptor.encrypt('123123', salt='hello')
    y = cryptor.decrypt(x, salt="hello")
    assert y == '123123'