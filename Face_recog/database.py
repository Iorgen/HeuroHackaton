from peewee import *
import MySQLdb
import time
import dateutil.parser
from peewee import *
import pymysql
import database_connection
pymysql.install_as_MySQLdb()


# create a peewee database instance -- our models will use this database to
# persist information
database = MySQLDatabase('deppression', user='root', password='12345678',
                         host='localhost', port=3306)


class BaseModel(Model):
    class Meta:
        database = database


# ------------------------------------------------ #
# словарь настроения
class Sentiments(BaseModel):
    sentiment_name = TextField()


# Общий словарь вопросов
class Questions(BaseModel):
    question = TextField()
    sentiment_id = ForeignKeyField(Sentiments, backref='Question')


# Словарь эмоций человека
class Emotion(BaseModel):
    emotion_name = TextField()
    Sentiment_id = ForeignKeyField(Sentiments, backref='Emotions')
# ------------------------------------------------ #


# Таблица пациентов
class Patient(BaseModel):
    name = CharField()
    surname = CharField()


# Таблица логов изменений настроения из видео
class ChangeLogRecords(BaseModel):
    patient_id = ForeignKeyField(Patient, backref='Changelog')
    current_emotion_id = ForeignKeyField(Emotion, backref='Changelog')
    change_date = DateTimeField()


# Таблица логов ответов пациента
class AnswerLogRecords(BaseModel):
    patient_id = ForeignKeyField(Patient, backref='AnswerLogRecord')
    real_emotion = ForeignKeyField(Questions, backref='AnswerLogRecord')
    answer_date = DateTimeField()





# {0:'angry',1:'disgust',2:'fear',3:'happy',
#                 4:'sad',5:'surprise',6:'neutral'}