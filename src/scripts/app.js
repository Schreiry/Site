

document.addEventListener('DOMContentLoaded', function() {

    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('search-results');


    let timeout = null;
    searchInput.addEventListener('input', function() {
        clearTimeout(timeout);
        const query = searchInput.value.trim();

        if (query.length < 2) {
            resultsContainer.innerHTML = '';
            
            return;
        }
        // Использование дебаунса для уменьшения количества запросов
        timeout = setTimeout(() => {
            fetch(`http://127.0.0.1:8080/?query=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    resultsContainer.innerHTML = '';
                    data.forEach(item => {
                        const div = document.createElement('div');
                        div.classList.add('search-result-item');
                        div.innerHTML = `<strong>${item.title}</strong> by ${item.author} - ${item.genre}`;
                        resultsContainer.appendChild(div);
                    });
                })
                .catch(error => {
                    console.error('Ошибка при поиске:', error);
                });
        }, 300); // задержка 300 мс
    });
});
