from .fields import BaseField, StringField
from .errors import ValidationError


class ParserMetaClass(type):
    
    def __new__(cls, name, bases, attrs):
        super_new = super().__new__
        field_data = {}
        for attr_name, attr_value in attrs.items():
            if hasattr(attr_value, "__class__") and \
                issubclass(attr_value.__class__, BaseField):
                if not attr_value.name:
                    attr_value.name = attr_name
                field_data[attr_name] = attr_value
        
        attrs['_fields'] = field_data
        return super_new(cls, name, bases, attrs)


class BaseParser(object):

    def __init__(self, **values):
        # copy https://github.com/MongoEngine/mongoengine/blob/v0.1.1/mongoengine/base.py#L168
        self._data = {}
        self._errors = {}
        for attr_name, attr_value in self._fields.items():
            if attr_name in values:
                setattr(self, attr_name, values.pop(attr_name))
            else:
                value = getattr(self, attr_name, None)
                setattr(self, attr_name, value)
    
    def is_valid(self):
        pass


class Parser(BaseParser, metaclass=ParserMetaClass):
    
    def is_valid(self):
        try:
            for attr_name, attr_value in self._fields.items():
                value = self._data.get(attr_name)
                attr_value.validate(value)
                if not isinstance(value, attr_value.type):
                    setattr(self, attr_name, attr_value.type(value))
            return True
        except ValidationError as e:
            self._errors[attr_name] = str(e)
            return False
    
    def errors(self):
        return self._errors
