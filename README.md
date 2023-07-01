# Exchanger BTC/USDT
### Описание
1. По API подключаться к криптобирже
2. Получать текущий курс BTC/USDT с этой биржи по нажатию кнопки "Получить"
3. При нажатии кнопки "Обменять BTC на USDT" или "Обменять USDT на BTC" переходит к оплате
### Технологии
python
aiogram
ccxt
python-dotenv 
Flask

### Запуск проекта
- Установите виртуальное окружение
- Активируйте его
- Установите зависимости из файла requirements.txt
- Запустите файл start.py
```
python -m venv venv

source venv/Scripts/activate
```

создайте файл code/secret.py и запешите в него:
```
TOKEN = 'токен_вашего_тг_бота' (с ковычками)
```
```
pip install -r requirements.txt

python code/main.py
```
### Автор
Богдан Сокольников
для "ООО БаксарНЕТ"