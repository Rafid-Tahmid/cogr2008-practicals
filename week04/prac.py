# prac.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def count_students():
    n_prac01 = 40
    n_prac02 = 20
    n_prac03 = 20
    n_prac04 = 40
    n = n_prac01 + n_prac02 + n_prac03 + n_prac04
    return str(n)

@app.route('/teacher')
def count_teachers():
    n_lecturer = 1
    n_tutor = 1
    n = n_lecturer + n_tutor
    return 'There are %d instructors' % (n)
