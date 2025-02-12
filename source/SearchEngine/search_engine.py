# search_engine.py
from sqlalchemy import or_
from database import Session, BookModel
from sqlalchemy.orm import joinedload

class SearchEngine:
    def __init__(self):
        self.session = Session()

    def search_books(self, query: str):
        """
        Производит поиск книг по введённой подстроке.
        Ищется по названию и ключевым словам.
        """
        if not query or len(query) < 1:
            return []
        pattern = f"%{query}%"
        # Выполняем запрос с предварительной загрузкой связанных объектов (автор, жанр)
        results = (self.session.query(BookModel)
                   .options(joinedload(BookModel.author), joinedload(BookModel.genre))
                   .filter(
                       or_(
                           BookModel.title.ilike(pattern),
                           BookModel.keywords.ilike(pattern)
                       )
                   )
                   .all())
        return results
