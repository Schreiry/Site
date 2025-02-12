# database.py
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

Base = declarative_base()

# Association table for many-to-many relationship between books and characters
book_character_association = Table(
    'book_character', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('character_id', Integer, ForeignKey('characters.id'))
)

class AuthorModel(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    biography = Column(Text)

    books = relationship("BookModel", back_populates="author")

class GenreModel(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)

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
    keywords = Column(Text)  # keywords separated by commas

    author = relationship("AuthorModel", back_populates="books")
    genre = relationship("GenreModel", back_populates="books")
    characters = relationship("CharacterModel", secondary=book_character_association, back_populates="books")

class CharacterModel(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)

    books = relationship("BookModel", secondary=book_character_association, back_populates="characters")

class HistoricalEventModel(Base):
    __tablename__ = 'historical_events'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    date = Column(String(50))

# Create a connection to the database (SQLite is used for local development)
engine = create_engine('sqlite:///books.db', echo=False)
Session = sessionmaker(bind=engine)

def init_db():
    """Initializes the database by creating all tables (if they don't exist)."""
    Base.metadata.create_all(engine)
