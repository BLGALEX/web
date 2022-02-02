## Инструкция по запуску api на linux

Устанавливаем poetry
> pip install poetry

Создаем папку для проекта, заходим в нее и запускаем команду 
> git clone https://github.com/BLGALEX/web.git

Заходим в папку репозитория и вводим запускаем установку зависимостей
> poetry install

Активируем виртуальную машину poetry, выполняем миграции и запускаем сервис
> poetry shell
> ./manage.py makemigrations
> ./manage.py migrate
> ./manage.py  runserver 0.0.0.0:5000

