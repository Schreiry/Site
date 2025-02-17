// File: src/modules/search/SearchEngine.h
#ifndef SEARCH_ENGINE_H
#define SEARCH_ENGINE_H

#include <string>
#include <vector>
#include <memory>

// Базовый класс для человека (например, автора)
class Person {
public:
    Person(const std::string &name) : name(name) {}
    virtual ~Person() {}
    virtual std::string getName() const { return name; }
protected:
    std::string name;
};

// Класс автора
class Author : public Person {
public:
    Author(const std::string &name) : Person(name) {}
    // Дополнительные данные (биография и т.п.) можно добавить здесь
};

// Базовый класс для медиаресурсов
class MediaItem {
public:
    MediaItem(const std::string &title, Author* author) : title(title), author(author) {}
    virtual ~MediaItem() {}
    virtual std::string getTitle() const { return title; }
    virtual Author* getAuthor() const { return author; }
protected:
    std::string title;
    Author* author;
};

// Класс книги
class Book : public MediaItem {
public:
    Book(const std::string &title, Author* author, const std::string &genre, const std::string &summary)
    : MediaItem(title, author), genre(genre), summary(summary) {}
    virtual std::string getGenre() const { return genre; }
    virtual std::string getSummary() const { return summary; }
private:
    std::string genre;
    std::string summary;
};

// Дополнительные сущности: Персонажи, Исторические события
class Character {
public:
    Character(const std::string &name, const std::string &role) : name(name), role(role) {}
    std::string getName() const { return name; }
    std::string getRole() const { return role; }
private:
    std::string name;
    std::string role;
};

class HistoricalEvent {
public:
    HistoricalEvent(const std::string &title, const std::string &description) : title(title), description(description) {}
    std::string getTitle() const { return title; }
    std::string getDescription() const { return description; }
private:
    std::string title;
    std::string description;
};

// Класс поискового движка, инкапсулирующий функциональность поиска
class SearchEngine {
public:
    SearchEngine();
    ~SearchEngine();
    
    // Функция поиска, возвращающая список книг по запросу
    std::vector<Book*> search(const std::string &query);
    
    // Метод для добавления книги в базу
    void addBook(Book* book);
    
    // Для демонстрации можно добавить методы для поиска персонажей, событий и т.п.
private:
    std::vector<Book*> books;
    
    // Простой метод ранжирования (заглушка для алгоритмов машинного обучения)
    int rankBook(Book* book, const std::string &query);
};

#endif // SEARCH_ENGINE_H
