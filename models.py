from peewee import *

db = PostgresqlDatabase("bcards", user="bcarduser", password="123")


class BaseModel(Model):
    class Meta:
        database = db

class TelegramUser(BaseModel):
    chat_id = IntegerField(unique=True)
    first_name = CharField(null=True, default="")
    address = CharField(null=True, default="")
    phone = IntegerField(null=True)
    deleted = BooleanField(default=False)
    state = CharField(default="main", null=False)

def initTables():
    db.connect()
    db.create_tables([TelegramUser], True)