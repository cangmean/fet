from fet.core.parser import Parser
from fet.core.parser.fields import StringField, IntField


class Person(Parser):

    name = StringField()
    age = IntField()


p = Person(name='mink', age='hello')

print(p.is_valid(), p.name, p.age, type(p.age))
print(p.errors())