# models.py
from abc import ABC, abstractmethod

class LiteraryEntity(ABC):
    @abstractmethod
    def get_info(self) -> str:
        """Возвращает строковое представление объекта."""
        pass

class Author(LiteraryEntity):
    def __init__(self, name: str, biography: str = ""):
        self.name = name
        self.biography = biography

    def get_info(self) -> str:
        return f"Автор: {self.name}"

class Genre(LiteraryEntity):
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description

    def get_info(self) -> str:
        return f"Жанр: {self.name}"

class Book(LiteraryEntity):
    def __init__(self, title: str, author: Author, genre: Genre,
                 style: str, century: str, plot: str, keywords: list):
        self.title = title
        self.author = author
        self.genre = genre
        self.style = style
        self.century = century
        self.plot = plot
        self.keywords = keywords  # список ключевых слов

    def get_info(self) -> str:
        return f"Книга: '{self.title}' автор {self.author.name} (Жанр: {self.genre.name})"
