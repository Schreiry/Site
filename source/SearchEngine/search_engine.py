# search_engine.py
import pymorphy2
from sqlalchemy import or_
from database import Session, BookModel, CharacterModel, HistoricalEventModel
from sqlalchemy.orm import joinedload

class SearchEngine:
    def __init__(self):
        self.session = Session()
        self.morph = pymorphy2.MorphAnalyzer()
        # Простая база синонимов для демонстрации (можно расширять)
        self.synonyms = {
            'война': ['битва', 'конфликт'],
            'любовь': ['страсть', 'романтика']
        }
    
    def normalize_text(self, text: str) -> str:
        """
        Приводит текст к нижнему регистру и нормализует каждое слово с помощью морфологического анализа.
        """
        tokens = text.lower().split()
        normalized = [self.morph.parse(token)[0].normal_form for token in tokens]
        return " ".join(normalized)
    
    def expand_query(self, query: str) -> str:
        """
        Расширяет запрос, добавляя синонимы из словаря.
        """
        tokens = query.lower().split()
        expanded_tokens = set(tokens)
        for token in tokens:
            if token in self.synonyms:
                for syn in self.synonyms[token]:
                    expanded_tokens.add(syn)
        return " ".join(expanded_tokens)
    
    def dummy_ml_ranker(self, items, query_tokens):
        """
        Демонстрационная функция ранжирования, которая начисляет баллы за совпадения токенов в текстовых полях.
        В реальной системе здесь может быть обученная модель (например, на основе TF-IDF или нейросети).
        """
        ranked = []
        for item in items:
            score = 0
            content = ""
            # Если объект – книга, учитываем её поля
            if hasattr(item, 'title'):
                content += f" {item.title}"
            if hasattr(item, 'keywords') and item.keywords:
                content += f" {item.keywords}"
            if hasattr(item, 'plot') and item.plot:
                content += f" {item.plot}"
            content = content.lower()
            for token in query_tokens:
                if token in content:
                    score += 1
            ranked.append((score, item))
        ranked.sort(key=lambda x: x[0], reverse=True)
        return [item for score, item in ranked]
    
    def search(self, query: str):
        """
        Производит поиск по книгам, персонажам и историческим событиям.
        Используется морфологический анализ для нормализации запроса, расширение синонимами и демонстрационное ранжирование.
        """
        if not query or len(query.strip()) == 0:
            return []
        
        # Нормализуем и расширяем запрос
        normalized_query = self.normalize_text(query)
        expanded_query = self.expand_query(normalized_query)
        query_tokens = expanded_query.split()
        
        # Формируем шаблоны для поиска (LIKE-паттерны)
        patterns = [f"%{token}%" for token in query_tokens]
        
        # Поиск в книгах (загрузка связанных объектов: автор, жанр)
        books_query = self.session.query(BookModel).options(
            joinedload(BookModel.author), joinedload(BookModel.genre)
        ).filter(
            or_(
                *[BookModel.title.ilike(pattern) for pattern in patterns],
                *[BookModel.keywords.ilike(pattern) for pattern in patterns],
                *[BookModel.plot.ilike(pattern) for pattern in patterns]
            )
        ).all()
        
        # Поиск в персонажах
        characters_query = self.session.query(CharacterModel).filter(
            or_(
                *[CharacterModel.name.ilike(pattern) for pattern in patterns],
                *[CharacterModel.description.ilike(pattern) for pattern in patterns]
            )
        ).all()
        
        # Поиск в исторических событиях
        events_query = self.session.query(HistoricalEventModel).filter(
            or_(
                *[HistoricalEventModel.name.ilike(pattern) for pattern in patterns],
                *[HistoricalEventModel.description.ilike(pattern) for pattern in patterns]
            )
        ).all()
        
        # Объединяем результаты и применяем ранжирование
        all_results = books_query + characters_query + events_query
        ranked_results = self.dummy_ml_ranker(all_results, query_tokens)
        return ranked_results
