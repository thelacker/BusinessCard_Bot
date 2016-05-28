from peewee import *
import os

db = SqliteDatabase(os.path.join(os.path.dirname(os.path.realpath(__file__)),'telegrambot.db'))

class BaseModel(Model):
    class Meta:
        database = db

class TelegramUser(BaseModel):
    chat_id = IntegerField(unique=True)
    first_name = CharField(null=True, default="")
    post = CharField(null=True, default="")
    phone = CharField(null=True)
    email = CharField(null=True, default="")
    deleted = BooleanField(default=False)
    state = CharField(default="main", null=False)

def initTables():
    db.connect()
    db.create_tables([TelegramUser], True)