# main.py
from flask import Flask, request, jsonify, render_template
from database import init_db, Session, AuthorModel, GenreModel, BookModel, CharacterModel, HistoricalEventModel
from search_engine import SearchEngine

app = Flask(__name__)
init_db()  # Инициализация базы данных

def seed_database():
    session = Session()
    if session.query(AuthorModel).count() == 0:
        # Добавляем тестовые данные
        author1 = AuthorModel(name="Лев Толстой", biography="Русский писатель, автор 'Войны и мира'.")
        genre1 = GenreModel(name="Роман", description="Эпический роман")
        book1 = BookModel(
            title="Война и мир",
            style="Эпический",
            century="19 век",
            plot="Эпическая история на фоне Отечественной войны 1812 года",
            keywords="война, мир, любовь",
            author=author1, genre=genre1
        )
        # Добавляем персонажей, связанных с книгой
        character1 = CharacterModel(name="Пьер Безухов", description="Один из главных героев романа.")
        character2 = CharacterModel(name="Наташа Ростова", description="Молодая женщина, олицетворяющая любовь и страсть.")
        book1.characters = [character1, character2]
        
        # Историческое событие
        event1 = HistoricalEventModel(
            name="Отечественная война 1812 года",
            description="Военные действия против наполеоновской армии.",
            date="1812"
        )
        
        session.add_all([author1, genre1, book1, character1, character2, event1])
        session.commit()
    session.close()

seed_database()

search_engine = SearchEngine()

@app.route('/')
def index():
    """Отображает главную страницу с формой поиска."""
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    """
    API-эндпоинт для поиска.
    Принимает GET-параметр 'q' (запрос пользователя) и возвращает найденные объекты в формате JSON.
    """
    query = request.args.get('q', '')
    results = search_engine.search(query)
    output = []
    for item in results:
        item_type = ""
        if hasattr(item, 'title'):
            item_type = "book"
            info = {
                'id': item.id,
                'title': item.title,
                'author': item.author.name if item.author else "",
                'genre': item.genre.name if item.genre else "",
                'style': item.style,
                'century': item.century,
                'plot': item.plot,
                'keywords': [kw.strip() for kw in item.keywords.split(',')] if item.keywords else []
            }
        elif hasattr(item, 'description') and not hasattr(item, 'title'):
            # Различаем персонажей и исторические события
            if hasattr(item, 'date'):
                item_type = "historical_event"
                info = {
                    'id': item.id,
                    'name': item.name,
                    'description': item.description,
                    'date': item.date
                }
            else:
                item_type = "character"
                info = {
                    'id': item.id,
                    'name': item.name,
                    'description': item.description
                }
        else:
            info = {}
        output.append({'type': item_type, 'data': info})
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)
