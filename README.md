## Инструкция по запуску api на linux

Устанавливаем poetry
> pip install poetry

Создаем папку для проекта, заходим в нее и запускаем команду 
> git clone https://github.com/BLGALEX/web.git

Заходим в папку репозитория и запускаем установку зависимостей
> poetry install

Активируем виртуальную машину poetry, выполняем миграции и запускаем сервис
> poetry shell
> 
> ./manage.py makemigrations
> 
> ./manage.py migrate
> 
> ./manage.py  runserver 0.0.0.0:5000



## Скриншоты с использованием Postman

Регистрация пользователя
![Регистрация пользователя](https://user-images.githubusercontent.com/58458024/152281582-aef61d98-b92e-4131-bc25-3b5252e3841d.png)

Проверка, что пользователь зарегестрирован
![Проверка, что пользователь зарегестрирован](https://user-images.githubusercontent.com/58458024/152282623-67b90923-06e6-44db-a081-3dfec6e84232.png)

Добавление новой задачи
![Добавление новой задачи](https://user-images.githubusercontent.com/58458024/152282852-2332ef08-7f00-4e4a-a89b-bdb898f09c9d.png)


