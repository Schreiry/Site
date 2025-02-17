// File: src/core/api/SearchAPI.cpp
#include "SearchAPI.h"
#include <Poco/Net/HTTPServerResponse.h>
#include <Poco/Net/HTTPServerRequest.h>
#include <Poco/Net/HTMLForm.h>
#include <Poco/JSON/Array.h>
#include <Poco/JSON/Stringifier.h>
#include <sstream>

using namespace Poco::Net;
using namespace Poco::Util;
using namespace Poco::JSON;
using namespace std;
using std::string;

void SearchRequestHandler::handleRequest(HTTPServerRequest& request, HTTPServerResponse& response) {
    response.setContentType("application/json");
    // Получаем параметры запроса
    HTMLForm form(request, request.stream());
    std::string query = form.get("query", "");
    
    // Выполняем поиск в базе данных
    std::vector<Book*> results = searchEngine->search(query);
    
    // Формирование JSON-ответа
    Array arr;
    for(auto& book : results) {
        Object obj;
        obj.set("title", book->getTitle());
        obj.set("author", book->getAuthor()->getName());
        obj.set("genre", book->getGenre());
        // Можно добавить и другие данные
        arr.add(obj);
    }
    
    std::ostringstream oss;
    Stringifier::stringify(arr, oss);
    response.send() << oss.str();
}

SearchAPIServer::SearchAPIServer() {
    searchEngine = new SearchEngine();
}

SearchAPIServer::~SearchAPIServer() {
    delete searchEngine;
}

int SearchAPIServer::main(const vector<string>& args) {
    try {
        // Создание сокета на порту 8080
        Poco::UInt16 port = 8080;
        ServerSocket svs(port);
        HTTPServer server(new SearchRequestHandlerFactory(searchEngine), svs, new HTTPServerParams);
        server.start();
        waitForTerminationRequest();  // Ожидание завершения (CTRL-C)
        server.stop();
    } catch (std::exception &ex) {
        std::cerr << "Exception: " << ex.what() << std::endl;
        return Application::EXIT_SOFTWARE;
    }
    return Application::EXIT_OK;
}

// Точка входа приложения
int main(int argc, char** argv) {
    SearchAPIServer app;
    return app.run(argc, argv);
}
