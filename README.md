# spimex_petroleum_prices

1. Клонируйте репозиторий ена локал
2. Установите зависимости pip install -r requiremets.txt 

3. Для получения данных введите url 'http://127.0.0.1:80/spimex_prices'
и введите торговый день, за который нужно получить данные в формате '20230707'

Даты торговых дней можно посмотреть здесь: https://spimex.com/markets/oil_products/trades/results/

4. Create docker image: "docker build --tag spimex_petroleum_prices ."
5. Run docker: "docker run -p 81:80 spimex_petroleum_prices"
