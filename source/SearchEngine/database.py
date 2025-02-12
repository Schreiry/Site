# database.py
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

Base = declarative_base()

class AuthorModel(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    biography = Column(Text)

    # Связь с книгами
    books = relationship("BookModel", back_populates="author")

class GenreModel(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)

    # Связь с книгами
    books = relationship("BookModel", back_populates="genre")

class BookModel(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))
    genre_id = Column(Integer, ForeignKey('genres.id'))
    style = Column(String(255))
    century = Column(String(50))
    plot = Column(Text)
    keywords = Column(Text)  # ключевые слова через запятую

    # Связи с таблицами авторов и жанров
    author = relationship("AuthorModel", back_populates="books")
    genre = relationship("GenreModel", back_populates="books")

# Создание подключения к базе данных (здесь используется SQLite)
engine = create_engine('sqlite:///books.db', echo=False)
Session = sessionmaker(bind=engine)

def init_db():
    """Инициализирует базу данных (создаёт таблицы, если их нет)."""
    Base.metadata.create_all(engine)
