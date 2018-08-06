import warnings
import redis
from fet.utils import to_string


class _Session(object):

    def __init__(self, name, store, expires=None):
        self.name = name
        self.store = store
        self._expires = expires

    def make_key(self, key):
        if not self.name:
            return key
        else:
            return "{}:{}".format(self.name, key)

    def set(self, key, value, expires=None):
        key = self.make_key(key)
        if expires:
            self.store.set(key, value, expires)
        elif self._expires:
            self.store.set(key, value, self._expires)
        else:
            self.store.set(key, value)

    def get(self, key):
        key = self.make_key(key)
        return to_string(self.store.get(key))

    def exists(self, key):
        key = self.make_key(key)
        if self.store.exists(key):
            return True
        else:
            return False


class Session(object):
    
    def __init__(self, app=None, store=None):
        if app is not None:
            self.init_app(app, store)
        
    def init_app(self, app, store=None):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        
        if store:
            self.store = store

        app.config.setdefault('FET_SESSION_STORE', None)
        app.config.setdefault('FET_SESSION_NAME', None)
        app.config.setdefault('FET_SESSION_EXPIRES', None)
        
        if not (self.store or app.config['FET_SESSION_STORE']):
            warnings.warn(
                "Session store or config `FET_SESSION_STORE` not defined.",
                Warning
            )

        app.extensions['fet_session'] = self
        self.session = self.get_session(app)
    
    def get_session(self, app):
        return _Session(
            name=app.config['FET_SESSION_NAME'],
            store=self.store or redis.Redis(app.config['FET_SESSION_STORE']),
            expires=app.config['FET_SESSION_EXPIRES']
        )

    def get(self, key):
        return self.session.get(key)
    
    def set(self, key, value, expires=None):
        self.session.set(key, value, expires)

    def exists(self, key):
        return self.session.exists(key)