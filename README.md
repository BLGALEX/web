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

Получение списка задач
![Получение списка задач](https://user-images.githubusercontent.com/58458024/152283045-150edd52-966c-45e3-8be9-332fefd562e4.png)

Изменение полей задачи (title и/или complete)
![Изменение полей задачи](https://user-images.githubusercontent.com/58458024/152283256-cb696979-5d49-486d-9536-fb3ca38873f0.png)

Удаление задачи
![image](https://user-images.githubusercontent.com/58458024/152283325-933d2261-d87f-4b3f-b16f-44dc58a03036.png)
