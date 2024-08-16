# Интернет-магазин


## Структура проекта
### Проект состит из следующих частей
1. Приложения:
 - `basket_app` - приложение подготовка к оформлению заказа, корзина для хранения продуктов, 
    как у зарегистрированных пользователей, так и у тех кто не прошел аутентификацию;
 - `catalog_app` - приложение товаров магазина, сортировка товара;
 - `shopapp_app` - приложение заказов, продуктов, тегов и оплата товаров;
 - `myauth_app` - приложение пользователей и личного кабинета;
2. Директории шаблонов:
 - `templates`;
3. Документация:
 - `Readme` - директория документации;
 - `Requirements` - директория зависимостей;
4. Служебные директории:
 - `fixtures` - фикстуры с тестовыми данными для заполнения сайта контентом;
 - `static` - статичные файлы сайта;
 - `upload` - директория для загружаемых моделями файлов;
5. Системные и служебные файлы:
 - `config` - директория настроек django-проекта;

Документация по каждому из приложений расположена в директории `Readme`.

## Установка проекта
Для установки исходника интернет магазина необходимо ввести следующую команду:

Выполните миграцию БД:
```
python manage.py migrate
```
Скопируйте фикстуры для заполнения базы данных:
```
python manage.py loaddata categories_fixtures.json users.json profile_fixtures.json product_fixtures.json productimage_fixtures.json review_fixtures.json tag_fixtures.json sales_fixtures.json productspecification_fixtures.json order_fixtures.json payment_fixtures.json
```
Запустить проект можно в докере, дял этого выполните 

```
docker compose up
```
Запустить проект можно локально

```
python manage.py runserver
```

При этом будут созданы 2 пользователей со следующими данными:

| Логин для входа | Пароль   | Группа       |
|-----------------|----------|--------------|
| admin           | 1        | superuser    | 
| test1           | 1        | Пользователь |

Документация сайта:

```
http://localhost/api/api-docs/

```
- localhost - IP-адрес проекта 




