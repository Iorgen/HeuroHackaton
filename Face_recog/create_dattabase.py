from peewee import *
import database


def create_tables():
    with database.database:
        database.database.create_tables([database.Sentiments, database.Questions, database.Emotion, database.ChangeLogRecords, database.AnswerLogRecords, database.Patient ])


if __name__ == "__main__":
    create_tables()