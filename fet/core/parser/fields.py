from .errors import ValidationError


class BaseField(object):

    def __init__(
        self,
        name=None,
        required=False,
        default=None,
        type=None,
        validation=None,
        choices=None,
        help=None,
        **kwargs
    ):
        """
        :param name: 字段名
        :param required: 字段是否是必须的
        :param default: 字段默认值
        :param type: 字段默认类型
        :param validation: 字段验证函数
        :param choices: 字段值为choices中的内容
        :param help: 报错显示信息
        """
        self.name = name
        self.required = required
        self.default = default
        self.type = type
        self.validation = validation
        self.choices = choices
        self.help = help
    
    def error(self, message, **kwargs):
        raise ValidationError(message, **kwargs)
    
    def validate(self, value, **kwargs):
        """ 需要子类去实现"""
        raise NotImplementedError('Validate not implement.')
    
    def _validate_choices(self, value):
        """ 验证可选项
        """
        # copy https://github.com/MongoEngine/mongoengine/blob/master/mongoengine/base/fields.py#L198
        if not isinstance(self.choices, (list, tuple)):
            raise ValueError('validation argument for choices must be a '
                            'list or tuple.')
        
        if value not in self.choices:
            raise ValueError(
                'Value must be an isinstance of %s' % str(self.choices)
            )
    
    def _validate(self, value, **kwargs):
        """ 验证"""
        # copy https://github.com/MongoEngine/mongoengine/blob/master/mongoengine/base/fields.py#L221
        if self.choices:
            self._validate_choices(value)
        
        if self.validation is not None:
            if callable(self.validation):
                if not self.validation(value):
                    self.error('Value does not match custom validation method')
            else:
                raise ValueError('validation argument for "%s" must be a '
                                 'callable.' % self.name)
        
        if self.required and value is None:
            raise self.error('`%s` must be required' % self.name)

    def __get__(self, instance, owner):
        # copy https://github.com/MongoEngine/mongoengine/blob/v0.1.1/mongoengine/base.py#L20
        if instance is None:
            return self

        value = instance._data.get(self.name)
        if value is None:
            value = self.default
            if callable(value):
                value = value()
        return value
    
    def __set__(self, instance, value):
        # copy https://github.com/MongoEngine/mongoengine/blob/v0.1.1/mongoengine/base.py#L37
        instance._data[self.name] = value


class StringField(BaseField):
    
    field_type = str

    def __init__(self, min_length=None, max_length=None, **kwargs):
        self.min_length = min_length
        self.max_length = max_length
        kwargs['type'] = self.field_type
        super().__init__(**kwargs)

    def validate(self, value):
        self._validate(value)
        if value is not None:
            try:
                value = str(value)
            except TypeError:
                self.error('`%s` could not be converted to string' % self.name)


class IntField(BaseField):
    
    field_type = int

    def __init__(self, min_value=None, max_value=None, **kwargs):
        self.min_value = min_value
        self.max_value = max_value
        kwargs['type'] = self.field_type
        super().__init__(**kwargs)

    def validate(self, value):
        # copy https://github.com/MongoEngine/mongoengine/blob/master/mongoengine/fields.py#L260
        self._validate(value)
        if value is not None:
            print(12, value)
            try:
                value = int(value)
            except Exception:
                self.error('`%s` could not be converted to int' % value)


class BoolField(BaseField):
    
    field_type = bool

    def __init__(self, **kwargs):
        kwargs['type'] = self.field_type

    def validate(self, value):
        if not isinstance(value, bool):
            self.error('BooleanField only accepts boolean values')
