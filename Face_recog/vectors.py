import numpy as np
from database import *


def synchronize(vec_real, vec_pred):
    if len(vec_real) == len(vec_pred):
        return

    if len(vec_real) < len(vec_pred):
        res = []
        res.extend(vec_real)
        res.extend(vec_pred[len(vec_real)+1:])
        vec_real = np.array(res)
    else:
        res = []
        res.extend(vec_pred)
        res.extend(vec_real[len(vec_pred)+1])
        vec_pred = np.array(res)

    return vec_real, vec_pred


def equals_of_vectors(vector_real, vector_predict):
    if len(vector_predict) != len(vector_predict):
        vector_real, vector_predict = synchronize(vector_real, vector_predict)

    norm1 = np.linalg.norm(vector_real, 2)
    norm2 = np.linalg.norm(vector_predict, 2)

    return (norm1 - norm2)/(norm1 + norm2)


def predictDeppression(patient_id):
    real = np.array([])
    pred = np.array([])
    answerlogs = AnswerLogRecords.select().where(AnswerLogRecords.patient_id == patient_id)
    for answer in answerlogs:
        question = Questions.select().where(Questions.id == answer.real_emotion).get()
        np.append(real, question.sentiment_id)
        # print(answer.real_emotion)

    print(real)
    changelogs = ChangeLogRecords.select().where(ChangeLogRecords.patient_id == patient_id)
    for change in changelogs:
        print(change.current_emotion_id)
        question = Questions.select().where(Questions.id == change.current_emotion_id).get()
        np.append(pred, question.Sentiment_id)
        print(question.sentiment_id)
        # print(change.current_emotion_id)
    return real,pred

if __name__ == '__main__':
    real = np.array([1, 2, 1, 2,1,0,1,1,2,0,0,2,1,2,2,1,2,0,2,1])
    pred = np.array([1, 2, 1, 2,1,0,0,1,2,1,0,1,1,0,2,1,2,1,2,1])
    print(equals_of_vectors(real, pred))
