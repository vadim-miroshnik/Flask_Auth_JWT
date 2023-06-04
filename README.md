Cервис авторизации с системой ролей, написанный на Flask с использованием gevent. 

## API для сайта и личного кабинета

- регистрация пользователя;
- вход пользователя в аккаунт (обмен логина и пароля на пару токенов: JWT-access токен и refresh токен); 
- обновление access-токена;
- выход пользователя из аккаунта;
- изменение логина или пароля (с отправкой email вы познакомитесь в следующих модулях, поэтому пока ваш сервис должен позволять изменять личные данные без дополнительных подтверждений);
- получение пользователем своей истории входов в аккаунт;

## API для управления доступами

- CRUD для управления ролями:
  - создание роли,
  - удаление роли,
  - изменение роли,
  - просмотр всех ролей.
- назначить пользователю роль;
- отобрать у пользователя роль;
- метод для проверки наличия прав у пользователя. 


### Как запустить проект 
**Для запуска проекта следует скопировать файл .env.example и переименовать на .env**
```commandline
cp .env .env.example
cp db.env db.env.example
```

**Запустить проект с помощью Docker**
```commandline
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up
```

**Для создания суперпользователя**
```commandline
flask create_admin admin1 password1
```

**После запуска проекта, у вас будет доступ к [документации проекта](http://localhost:5000/apidocs/)**
