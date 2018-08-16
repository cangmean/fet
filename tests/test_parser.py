from fet.core.parser import Parser
from fet.core.parser.fields import StringField, IntField


class Person(Parser):

    name = StringField()
    age = IntField(default=3)


p = Person()

print(p.is_valid(), p.name, p.age, type(p.age))
print(p.parse_error())
print(p.parse_data())