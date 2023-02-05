from peewee import *


db = SqliteDatabase('data.db')


class User(Model):
    class Meta:
        database = db
        db_taple = 'User'
    vk_id = IntegerField()
    warns = IntegerField()
    mute = IntegerField()
    admin = IntegerField()
    black = IntegerField()

if __name__ == '__main__':
    db.create_tables([User])
