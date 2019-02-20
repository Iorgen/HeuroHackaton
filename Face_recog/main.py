#!/usr/bin/env python
#
# Project: Video Streaming with face recognition
# Author: agametov [at] gmail [dot] com>
# Date: 2016/02/11
# Website: http://www.agametov.ru/
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.
from random import randint
import datetime
from flask import Flask, render_template, Response, request, jsonify
from camera import VideoCamera
from database import *
app = Flask(__name__)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# --------------------- patient methods ------------------------ #
# API добавляющий пациента  - READY
@app.route('/add_patient')
def add_patient(name, surname):
    patient = Patient(name=name,
                      surname=surname)
    patient.save()
    return render_template('recorder.html')


# Метод получения результатов анализа
@app.route('/get_analysis_results' ,  methods = ['POST', 'GET'])
def get_analysis_results():
    # TODO return JSON with info and graphic image
    return render_template('test.html')


#  получения графика изменений настроения пациента вместе с ответами пациента
# @app.route('/patient_change_plot' ,  methods = ['POST'])
# def patient_change_plot(patient_id):
#     # TODO return JSON with info and graphic image
#     return render_template('recorder.html')


# --------------------------------------------- #
# Отображение страницы анализа по пациенту - READY
@app.route('/patient_analysis', methods = ['POST', 'GET'] )
def patient_analysis():
    patient_id = request.args.get('patient_id', default=1, type=int)
    patient = Patient.select().where(Patient.id == patient_id).get()
    return render_template('recorder.html', patient=patient)


# Главная страница сервиса депрессии - READY
@app.route('/')
def index():
    patients = Patient.select()
    return render_template('index.html', patients=patients)


# API отображающий видео транляцию с камеры - READY
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# ------------------ test methods  -------------------------- #
# Метод получения рандомного теста для проведения эксперимента - READY
@app.route('/get_random_test',  methods = ['POST', 'GET'])
def get_random_test():
    test_id = randint(383, 498)
    question = Questions.select().where(Questions.id == test_id).join(Sentiments).get()
    print(question.sentiment_id.sentiment_name)
    return render_template('test.html', question=question)


# Метод логирования ответов на тест для проведения эксперимента - READY
@app.route('/log_test_answer',  methods = ['POST', 'GET'])
def log_test_answer():
    patient_id = request.args.get('patient_id', default=1, type=int)
    test_id = request.args.get('test_id', default=1, type=int)
    question = Questions.select().where(Questions.id == test_id).get()
    answerlogrecord = AnswerLogRecords(patient_id=patient_id,
                                       real_emotion=question,
                                        answer_date=datetime.datetime.now())
    answerlogrecord.save()
    resp = jsonify(success=True)
    return resp


if __name__ == '__main__':
    app.run(debug=True)
