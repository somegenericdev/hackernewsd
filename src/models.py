from enum import Enum
from peewee import Model, CharField, DateField, AutoField, IntegerField, DatabaseProxy, DateTimeField


class BaseModel(Model):
    class Meta:
        database = DatabaseProxy()

class StoryType(Enum):
    Hackernews = 1
    Lobsters = 2

class Story(BaseModel):
    id = AutoField()   #autoincrement
    title = CharField()
    url = CharField(null=True)
    hnurl = CharField()
    last_seen = DateTimeField()
    posted_date = DateTimeField()
    type = IntegerField(choices=[(type.value, type.name) for type in StoryType], default=StoryType.Hackernews.value)
