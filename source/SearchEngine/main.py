# main.py
from flask import Flask, request, jsonify, render_template
from database import init_db, Session, AuthorModel, GenreModel, BookModel, CharacterModel, HistoricalEventModel
from search_engine import SearchEngine

app = Flask(__name__)
init_db()  # Initialize the database

def seed_database():
    session = Session()
    if session.query(AuthorModel).count() == 0:
        # Add test data
        author1 = AuthorModel(name="Leo Tolstoy", biography="Russian writer, author of 'War and Peace'.")
        genre1 = GenreModel(name="Roman", description="An epic novel")
        book1 = BookModel(
            title="war and peace",
            style="Epic",
            century="19th century",
            plot="An epic story set against the backdrop of the Patriotic War of 1812",
            keywords="war, peace, love",
            author=author1, genre=genre1
        )
        # Add characters related to the book
        character1 = CharacterModel(name="Pierre Bezukhov", description="One of the main characters in the novel.")
        character2 = CharacterModel(name="Natasha Rostova", description="A young woman who epitomizes love and passion.")
        book1.characters = [character1, character2]
        
        # Historical event
        event1 = HistoricalEventModel(
            name="Russian War of 1812",
            description="Military action against Napoleon's army.",
            date="1812"
        )
        
        session.add_all([author1, genre1, book1, character1, character2, event1])
        session.commit()
    session.close()

seed_database()

search_engine = SearchEngine()

@app.route('/')
def index():
    """Displays the main page with the search form."""
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    """
    API endpoint for search.
    Accepts GET parameter 'q' (user query) and returns found objects in JSON format.
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
            # Distinguish between characters and historical events
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
