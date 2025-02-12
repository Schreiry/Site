# main.py
from flask import Flask, request, jsonify, render_template
from database import init_db, Session, AuthorModel, GenreModel, BookModel
from search_engine import SearchEngine

app = Flask(__name__)
init_db()  # Инициализация базы данных при запуске приложения

# Для демонстрации заполним базу тестовыми данными (если таблицы пустые)
def seed_database():
    session = Session()
    if session.query(AuthorModel).count() == 0:
        # Создаем тестовых авторов, жанры и книги
        author1 = AuthorModel(name="Лев Толстой", biography="Русский писатель, автор 'Войны и мира'.")
        genre1 = GenreModel(name="Роман", description="Большой художественный роман")
        book1 = BookModel(title="Война и мир",
                          style="Эпический",
                          century="19 век",
                          plot="Эпическая история на фоне Отечественной войны 1812 года",
                          keywords="война, мир, любовь, судьба",
                          author=author1, genre=genre1)
        session.add_all([author1, genre1, book1])
        session.commit()
    session.close()

seed_database()

search_engine = SearchEngine()

@app.route('/')
def index():
    # Отображаем главную страницу с формой поиска
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = search_engine.search_books(query)
    # Преобразуем результаты в удобный для JSON формат
    books = []
    for book in results:
        books.append({
            'id': book.id,
            'title': book.title,
            'author': book.author.name if book.author else "",
            'genre': book.genre.name if book.genre else "",
            'style': book.style,
            'century': book.century,
            'plot': book.plot,
            'keywords': [kw.strip() for kw in book.keywords.split(',')] if book.keywords else []
        })
    return jsonify(books)

if __name__ == '__main__':
    app.run(debug=True)
