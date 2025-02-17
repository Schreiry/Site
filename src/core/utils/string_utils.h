// File: src/core/utils/string_utils.h
#ifndef STRING_UTILS_H
#define STRING_UTILS_H

#include <string>
#include <algorithm>

namespace StringUtils {
    // Преобразование строки в нижний регистр
    inline std::string toLower(const std::string &input) {
        std::string output = input;
        std::transform(output.begin(), output.end(), output.begin(), ::tolower);
        return output;
    }
    
    // Проверка, начинается ли строка с заданного префикса
    inline bool startsWith(const std::string &str, const std::string &prefix) {
        return str.substr(0, prefix.size()) == prefix;
    }
    
    // Проверка, содержит ли строка подстроку
    inline bool contains(const std::string &str, const std::string &substr) {
        return str.find(substr) != std::string::npos;
    }
}

#endif // STRING_UTILS_H
