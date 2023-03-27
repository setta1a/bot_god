import peewee
from first.models import *


def create_tables():
    try:
        psql_db.connect()
        User.create_table()
        BotFunctions.create_table()
    except peewee.InternalError as px:
        print(str(px))
