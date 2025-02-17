// Directive space : 
#ifndef SEARCH_ENGINE_H
#define SEARCH_ENGINE_H

#include <string>
#include <vector>
#include <memory>


// ----             ----
using std::string;



// ----             ----




// Базовый класс для человека (например, автора)
class Person {
public:
    Person(const string &name) : name(name) {}
    virtual ~Person() {}
    virtual string getName() const { return name; }
protected:
    string name;
};

// Класс автора
class Author : public Person {
public:
    Author(const string &name) : Person(name) {}
    // Дополнительные данные (биография и т.п.) можно добавить здесь
};

// Базовый класс для медиаресурсов
class MediaItem {
public:
    MediaItem(const string &title, Author* author) : title(title), author(author) {}
    virtual ~MediaItem() {}
    virtual string getTitle() const { return title; }
    virtual Author* getAuthor() const { return author; }
protected:
    string title;
    Author* author;
};

// Класс книги
class Book : public MediaItem {
public:
    Book(const string &title, Author* author, const string &genre, const string &summary)
    : MediaItem(title, author), genre(genre), summary(summary) {}
    virtual string getGenre() const { return genre; }
    virtual string getSummary() const { return summary; }
private:
    string genre;
    string summary;
};

// Дополнительные сущности: Персонажи, Исторические события
class Character {
public:
    Character(const string &name, const string &role) : name(name), role(role) {}
    string getName() const { return name; }
    string getRole() const { return role; }
private:
    string name;
    string role;
};

class HistoricalEvent {
public:
    HistoricalEvent(const string &title, const string &description) : title(title), description(description) {}
    string getTitle() const { return title; }
    string getDescription() const { return description; }
private:
    string title;
    string description;
};

// Класс поискового движка, инкапсулирующий функциональность поиска
class SearchEngine {
public:
    SearchEngine();
    ~SearchEngine();
    
    // Функция поиска, возвращающая список книг по запросу
    std::vector<Book*> search(const string &query);
    
    // Метод для добавления книги в базу
    void addBook(Book* book);
    
    // Для демонстрации можно добавить методы для поиска персонажей, событий и т.п.
private:
    std::vector<Book*> books;
    
    // Простой метод ранжирования (заглушка для алгоритмов машинного обучения)
    int rankBook(Book* book, const string &query);
};

#endif // SEARCH_ENGINE_H
