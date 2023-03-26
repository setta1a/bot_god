from peewee import *  # pip install peewee
import datetime

psql_db = PostgresqlDatabase('bot_god', user='postgres', password='postgres', host='localhost')


class BaseModel(Model):
    class Meta:
        database = psql_db


class User(BaseModel):
    id = PrimaryKeyField(null=False)
    first_name = CharField()
    last_name = CharField()
    username = CharField()
    photo_url = CharField()
    auth_date = DateTimeField(default=datetime.datetime.now())
    hash = CharField()


class BotFunctions(BaseModel):
    func_name = CharField(max_length=64)
    file_name = CharField(max_length=64)
