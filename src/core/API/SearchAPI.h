// File: src/core/api/SearchAPI.h
#ifndef SEARCH_API_H
#define SEARCH_API_H

#include "../modules/search/SearchEngine.h"  // Подключение поискового движка
#include <Poco/Net/HTTPRequestHandler.h>
#include <Poco/Net/HTTPServer.h>
#include <Poco/Net/ServerSocket.h>
#include <Poco/Net/HTTPRequestHandlerFactory.h>
#include <Poco/Util/ServerApplication.h>
#include <Poco/JSON/Object.h>
#include <string>

// Обработчик HTTP-запросов для поиска
class SearchRequestHandler : public Poco::Net::HTTPRequestHandler {
public:
    SearchRequestHandler(SearchEngine* engine) : searchEngine(engine) {}
    void handleRequest(Poco::Net::HTTPServerRequest& request, Poco::Net::HTTPServerResponse& response) override;
private:
    SearchEngine* searchEngine;
};

class SearchRequestHandlerFactory : public Poco::Net::HTTPRequestHandlerFactory {
public:
    SearchRequestHandlerFactory(SearchEngine* engine) : searchEngine(engine) {}
    Poco::Net::HTTPRequestHandler* createRequestHandler(const Poco::Net::HTTPServerRequest& request) override {
        return new SearchRequestHandler(searchEngine);
    }
private:
    SearchEngine* searchEngine;
};

// Основное приложение API-сервера
class SearchAPIServer : public Poco::Util::ServerApplication {
public:
    SearchAPIServer();
    ~SearchAPIServer();
protected:
    int main(const std::vector<std::string>& args) override;
private:
    SearchEngine* searchEngine;
};

#endif // SEARCH_API_H
