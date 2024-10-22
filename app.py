from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Инициализация приложения
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'  # Путь к базе данных
db = SQLAlchemy(app)

# Модель для хранения данных о фильмах
class Movie(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    opisanie = db.Column(db.Text)
    release_date = db.Column(db.Date)
    time = db.Column(db.Integer)
    poster_url = db.Column(db.String(255))

# Главная страница с отображением списка фильмов
@app.route("/")
def index():
    movies = Movie.query.all()  # Получаем все фильмы из базы данных
    return render_template("index.html", movies=movies)

# Страница для добавления нового фильма
@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Получаем данные из формы
        title = request.form['title']
        opisanie = request.form['opisanie']
        release_date = request.form['release_date']
        time = request.form['time']
        poster_url = request.form['poster_url']

        # Преобразуем строку даты в объект datetime
        release_date = datetime.strptime(release_date, '%Y-%m-%d')

        # Создаем новый объект Movie и сохраняем в базу данных
        new_movie = Movie(
            title=title,
            opisanie=opisanie,
            release_date=release_date,
            time=time,
            poster_url=poster_url
        )
        db.session.add(new_movie)
        db.session.commit()

        # Перенаправляем на главную страницу после добавления фильма
        return redirect(url_for('index'))

    return render_template("create.html")  # Отображаем форму для добавления фильма

# Запуск приложения
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создаем таблицы, если они еще не созданы
        print("Таблицы созданы!")
    app.run(debug=True)
