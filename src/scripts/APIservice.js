// File: src/scripts/services/apiService.js
export function searchBooks(query) {
    return fetch(`http://127.0.0.1:8080/?query=${encodeURIComponent(query)}`)
        .then(response => response.json());
}
