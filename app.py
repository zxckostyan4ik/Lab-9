from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# настройка базы данных (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# модель базы данных
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    important = db.Column(db.Boolean, default=False)

# главная страница
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        important = True if request.form.get('important') else False

        new_note = Note(text=text, important=important)
        db.session.add(new_note)
        db.session.commit()

        return redirect('/')

    notes = Note.query.all()
    return render_template('index.html', notes=notes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # создаёт БД
    app.run(debug=True)