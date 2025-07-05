#Llamalo XD
from flask import Flask, redirect, url_for, session, request, render_template
from nomedigas import get_miku_q, get_the_mikus,check_my_mikus
import random
from random import shuffle
import os

folder= os.getcwd()
app = Flask(__name__,template_folder=folder, static_folder=folder)

def start_quiz(quiz_id):
    session['quiz'] = quiz_id
    session['last'] = 0
    session['correct'] = 0
    session['total'] = 0

def tha_quiz():
    quiz_list = get_the_mikus()
    options = []
    for quiz_id,quiz_name in quiz_list:
        options.append(f'<option value="{quiz_id}">{quiz_name}</options>')
    options_str = '\n'.join(options)
    return options_str


def index():
    if request.method == 'GET':
        form_html = tha_quiz()
        start_quiz(-1)
        return render_template('PPP.html', header = 'Welcome to the puzzle park',select = 'Selecciona wey :) : ',quizzes = get_the_mikus())
    else:
        quiz_z = int(request.form.get('quiz'))
        start_quiz(quiz_z)
        return redirect(url_for('test'))

def save_the_miqus():
    answer = request.form.get('ans_text')
    q_id = request.form.get('q_id')
    session['last'] = q_id
    session['total'] += 1

    if check_my_mikus(q_id,answer):
        session['correct'] += 1

def miku_form(question):
    answer_list = [question[2], question[3], question[4], question[5]]
    shuffle(answer_list)
    print(f"Pregunta: {question[1]}")
    print(f"Opciones de respuesta: {answer_list}")

    return render_template('test.html', q_id=question[0], question=question[1], answer_list=answer_list)

def test():
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            save_the_miqus()
        next_question = get_miku_q(session['last'], session['quiz'])
        if next_question is None or len(next_question) == 0:
            return redirect(url_for('result'))
        else:
            return miku_form(next_question)

def result():
    if session['total'] == 0:
        return '<h2>Gracias por participar</h2>'
    else:
        porcent = round((session['correct'] * 100) / session['total'])
        return render_template('result.html', header='Resultado del Quiz:', result=f"Respuestas Correctas: {session['correct']} de {session['total']}", porcent=f"Porcentaje de acierto: {porcent}%")


app.config['SECRET_KEY']= 'Shhhh'
app.add_url_rule('/','index',index, methods=['GET','POST'])
app.add_url_rule('/test','test',test)
app.add_url_rule('/result','result',result)
app.run()
