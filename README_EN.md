# Online Store


## Project structure
### The project consists of the following parts
1. Applications:
 - `basket_app` - application preparation for ordering, shopping cart for storing products, 
    both registered users and those who have not authenticated;
 - `catalog_app` - product store application, product sorting;
 - `shopapp_app` - an application for orders, products, tags and payment for goods;
 - `myauth_app` - application for users and personal account;
2. Template directory:
- `templates`;
3. Documentation:
 - 'Readme` - documentation catalog;
 - 'Requirements` - order catalog;
4. Service directories:
 - `fixtures` - fixtures with test data for filling the site with content;
 - 'static' - static site files;
 - 'upload` - directory for uploaded file models;
5. System and service files:
 - 'config` - django project settings directory;

Documentation for each of the applications is available in the `Readme` directory.

## Project Installation
To install the online store developer, enter the following command:

Perform a database migration:
```
python manage.py migrate
```
Copy the fixtures to fill the airbags:
```
python manage.py loaddata categories_fixtures.json users.json profile_fixtures.json product_fixtures.json productimage_fixtures.json review_fixtures.json tag_fixtures.json sales_fixtures.json productspecification_fixtures.json order_fixtures.json payment_fixtures.json
```
You can run the project in the docker, I did it 

```
docker compose up
```
You can run the project locally

```
python manage.py runserver
```

This will create 2 users with the following data:

| Login | Password | Group |
|-----------------|----------|--------------|
| admin           | 1        | superuser    | 
| test1 | 1 | User |

Documentation on the website:

```
http://localhost/api/api-docs/

```
- localhost-IP address of the project