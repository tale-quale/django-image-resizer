<h1>Инструкция по запуску на локальной машине:</h1>
Клонируем репозиторий:
<code>git clone https://github.com/tale-quale/django-image-resizer.git</code>
<br>
Создаем и активируем виртуальное окружение:
<code>virtualenv venv</code>
<code>virtualenv venv/bin/activate/</code>
<br>
Переходими в папку с проектом и устанавливаем зависимости:
<code>cd django-image-resizer</code>
<code>pip install -r requirements.txt</code>
<br>
Запускаем сервер:
<code>python3 manage.py runserver</code>
<br>
Открываем в браузере - http://127.0.0.1:8000/
