import sqlite3
db_name = 'quiz.sqlite'
conn = None
cursor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def clear_db():
    open()
    cursor.execute('''DROP TABLE IF EXISTS quiz_content''')
    cursor.execute('''DROP TABLE IF EXISTS question''')
    cursor.execute('''DROP TABLE IF EXISTS quiz''')
    conn.commit()
    close()

    
def create():
    open()
    do('''CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )''')
    do('''CREATE TABLE IF NOT EXISTS question (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        answer TEXT NOT NULL,
        wrong1 TEXT NOT NULL,
        wrong2 TEXT NOT NULL,
        wrong3 TEXT NOT NULL
    )''')
    do('''CREATE TABLE IF NOT EXISTS quiz_content (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        FOREIGN KEY (quiz_id) REFERENCES quiz (id),
        FOREIGN KEY (question_id) REFERENCES question (id)
    )''')

def miku_qui():
    open()
    quizzes = [
        ('el mas mejol',),
        ('el geek mas friki',),
        ('el fan mas normal de pokemon',)
    ]
    cursor.executemany("INSERT INTO quiz (name) VALUES (?)", quizzes)
    conn.commit()
    close()

def miku_que():
    open()
    questions = [
        ('si un objeto encima de un tren se mueve a 80 km por hora y el tren se mueve a 120 km por hora que dia va a ser el jueves', 'jueves', 'miercoles', '2600 m/s', 'jose'),
        ('cual fue la primera consola comercial de la historia', 'La magnabox', 'el atari', 'el famicon', 'A780'),
        ('cuantos pokemos existen', '1025', 'Vaporeon', 'por que','sigo haciendo esto :(')
    ]
    cursor.executemany("INSERT INTO question (name, answer, wrong1, wrong2, wrong3) VALUES (?,?,?,?,?)", questions)
    conn.commit()
    close()

def set_links():
    open()
    query = "INSERT INTO quiz_content (quiz_id, question_id) VALUES (?,?)"
    link = input("entrada no preguntes (y/n) ")
    while link.lower() == 'y':
        try:
            quiz_id = int(input('ID: '))
            question_id = int(input('ID-q: '))
            cursor.execute(query,[quiz_id, question_id])
            conn.commit()
        except ValueError:
            print("Valid ID")
        finally:
            link= input('Desea agregar(y/n) ')

def get_the_mikus():
    open()
    cursor.execute('SELECT * FROM quiz ORDER BY id')
    result = cursor.fetchall()
    close()
    return result

def get_miku_q(question_id=0,quiz_id=1):
    open()
    func = '''
    SELECT quiz_content.id, question.name, question.answer, 
    question.wrong1, question.wrong2, question.wrong3
    FROM  quiz_content, question
    WHERE quiz_content.question_id > (?) AND quiz_content.quiz_id= (?)
    AND quiz_content.question_id = question.id
    ORDER BY quiz_content.id
        '''
    cursor.execute(func,[question_id,quiz_id])
    result= cursor.fetchone()
    return result
    close()

def check_my_mikus(q_id, answer):
    query = '''
            SELECT question.answer
            FROM quiz_content, question
            WHERE quiz_content.id = ?
            AND quiz_content.question_id = question.id
        '''
    start()
    cursor.execute(query, (q_id,))
    result = cursor.fetchone()
    close()
    if result is None:
        return False
    else:
        if result[0] == answer:
            # print(result[0], ans_text)
            return True
        else:
            return False

def show(table):
    fun = 'SELECT * FROM ' + table
    open()
    cursor.execute(fun)
    print(cursor.fetchall())
    close()

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

def main():
    clear_db()
    create()
    miku_que()
    miku_qui()
    set_links()
    show_tables()
    print(get_miku_q)

if __name__ == "__main__":
    main()
