# Домашнее задание к занятию "6.2. SQL"

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 12) c 2 volume, 
в который будут складываться данные БД и бэкапы.

Приведите получившуюся команду или docker-compose манифест.

### Ответ:
```
# docker-compose манифест
version: "2.5"
networks:
  postgres:
    driver: bridge
services:
  postgres:
    image: postgres:12
    container_name: postgres
    environment: 
      - POSTGRES_HOST_AUTH_METHOD=trust
    volumes:
      - ~/devops/6.2-db-02-sql/ex1/data:/var/lib/postgresql/data
      - ~/devops/6.2-db-02-sql/ex1/backup:/var/lib/postgresql/backup
    restart: always
    networks:
      - postgres
    ports:
      - 5432:5432
```

## Задача 2

В БД из задачи 1: 
- создайте пользователя test-admin-user и БД test_db
- в БД test_db создайте таблицу orders и clients (спeцификация таблиц ниже)
- предоставьте привилегии на все операции пользователю test-admin-user на таблицы БД test_db
- создайте пользователя test-simple-user  
- предоставьте пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE данных таблиц БД test_db

Таблица orders:
- id (serial primary key)
- наименование (string)
- цена (integer)

Таблица clients:
- id (serial primary key)
- фамилия (string)
- страна проживания (string, index)
- заказ (foreign key orders)

Приведите:
- итоговый список БД после выполнения пунктов выше,
- описание таблиц (describe)
- SQL-запрос для выдачи списка пользователей с правами над таблицами test_db
- список пользователей с правами над таблицами test_db

### Ответ
```
1. итоговый список БД после выполнения пунктов выше

test_db=> \l
                                    List of databases
   Name    |      Owner      | Encoding |  Collate   |   Ctype    |   Access privileges   
-----------+-----------------+----------+------------+------------+-----------------------
 postgres  | postgres        | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0 | postgres        | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |                 |          |            |            | postgres=CTc/postgres
 template1 | postgres        | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |                 |          |            |            | postgres=CTc/postgres
 test_db   | test-admin-user | UTF8     | en_US.utf8 | en_US.utf8 | 
(4 rows)

2. описание таблиц (describe)

test_db=> \d orders
                                    Table "public.orders"
    Column    |       Type        | Collation | Nullable |              Default               
--------------+-------------------+-----------+----------+------------------------------------
 id           | integer           |           | not null | nextval('orders_id_seq'::regclass)
 наименование | character varying |           |          | 
 цена         | integer           |           |          | 
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "clients" CONSTRAINT "clients_заказ_fkey" FOREIGN KEY ("заказ") REFERENCES orders(id)


test_db=> \d clients
                                       Table "public.clients"
      Column       |       Type        | Collation | Nullable |               Default               
-------------------+-------------------+-----------+----------+-------------------------------------
 id                | integer           |           | not null | nextval('clients_id_seq'::regclass)
 фамилия           | character varying |           |          | 
 страна проживания | character varying |           |          | 
 заказ             | integer           |           |          | 
Indexes:
    "clients_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "clients_заказ_fkey" FOREIGN KEY ("заказ") REFERENCES orders(id)

3. SQL-запрос для выдачи списка пользователей с правами над таблицами test_db

test_db=> SELECT * FROM information_schema.table_privileges WHERE grantee = 'test-admin-user';
     grantor     |     grantee     | table_catalog | table_schema | table_name | privilege_type | is_grantable | with_hierarchy 
-----------------+-----------------+---------------+--------------+------------+----------------+--------------+----------------
 test-admin-user | test-admin-user | test_db       | public       | orders     | INSERT         | YES          | NO
 test-admin-user | test-admin-user | test_db       | public       | orders     | SELECT         | YES          | YES
 test-admin-user | test-admin-user | test_db       | public       | orders     | UPDATE         | YES          | NO
 test-admin-user | test-admin-user | test_db       | public       | orders     | DELETE         | YES          | NO
 test-admin-user | test-admin-user | test_db       | public       | orders     | TRUNCATE       | YES          | NO
 test-admin-user | test-admin-user | test_db       | public       | orders     | REFERENCES     | YES          | NO
 test-admin-user | test-admin-user | test_db       | public       | orders     | TRIGGER        | YES          | NO
 test-admin-user | test-admin-user | test_db       | public       | clients    | INSERT         | YES          | NO
 test-admin-user | test-admin-user | test_db       | public       | clients    | SELECT         | YES          | YES
 test-admin-user | test-admin-user | test_db       | public       | clients    | UPDATE         | YES          | NO
 test-admin-user | test-admin-user | test_db       | public       | clients    | DELETE         | YES          | NO
 test-admin-user | test-admin-user | test_db       | public       | clients    | TRUNCATE       | YES          | NO
 test-admin-user | test-admin-user | test_db       | public       | clients    | REFERENCES     | YES          | NO
 test-admin-user | test-admin-user | test_db       | public       | clients    | TRIGGER        | YES          | NO
(14 rows)

test_db=> SELECT * FROM information_schema.table_privileges WHERE grantee = 'test-simple-user';
     grantor     |     grantee      | table_catalog | table_schema | table_name | privilege_type | is_grantable | with_hierarchy 
-----------------+------------------+---------------+--------------+------------+----------------+--------------+----------------
 test-admin-user | test-simple-user | test_db       | public       | orders     | INSERT         | NO           | NO
 test-admin-user | test-simple-user | test_db       | public       | orders     | SELECT         | NO           | YES
 test-admin-user | test-simple-user | test_db       | public       | orders     | UPDATE         | NO           | NO
 test-admin-user | test-simple-user | test_db       | public       | orders     | DELETE         | NO           | NO
 test-admin-user | test-simple-user | test_db       | public       | clients    | INSERT         | NO           | NO
 test-admin-user | test-simple-user | test_db       | public       | clients    | SELECT         | NO           | YES
 test-admin-user | test-simple-user | test_db       | public       | clients    | UPDATE         | NO           | NO
 test-admin-user | test-simple-user | test_db       | public       | clients    | DELETE         | NO           | NO
(8 rows)

4. список пользователей с правами над таблицами test_db
test_db=> \dp clients
                                           Access privileges
 Schema |  Name   | Type  |              Access privileges              | Column privileges | Policies 
--------+---------+-------+---------------------------------------------+-------------------+----------
 public | clients | table | "test-admin-user"=arwdDxt/"test-admin-user"+|                   | 
        |         |       | "test-simple-user"=arwd/"test-admin-user"   |                   | 
(1 row)

test_db=> \dp orders
                                          Access privileges
 Schema |  Name  | Type  |              Access privileges              | Column privileges | Policies 
--------+--------+-------+---------------------------------------------+-------------------+----------
 public | orders | table | "test-admin-user"=arwdDxt/"test-admin-user"+|                   | 
        |        |       | "test-simple-user"=arwd/"test-admin-user"   |                   | 
(1 row)
```

## Задача 3

Используя SQL синтаксис - наполните таблицы следующими тестовыми данными:

Таблица orders

|Наименование|цена|
|------------|----|
|Шоколад| 10 |
|Принтер| 3000 |
|Книга| 500 |
|Монитор| 7000|
|Гитара| 4000|

Таблица clients

|ФИО|Страна проживания|
|------------|----|
|Иванов Иван Иванович| USA |
|Петров Петр Петрович| Canada |
|Иоганн Себастьян Бах| Japan |
|Ронни Джеймс Дио| Russia|
|Ritchie Blackmore| Russia|

Используя SQL синтаксис:
- вычислите количество записей для каждой таблицы 
- приведите в ответе:
    - запросы 
    - результаты их выполнения.

### Ответ
```
test_db=> SELECT COUNT(*) FROM orders;
 count 
-------
     5
(1 row)

test_db=> SELECT COUNT(*) FROM clients;
 count 
-------
     5
(1 row)
```

## Задача 4

Часть пользователей из таблицы clients решили оформить заказы из таблицы orders.

Используя foreign keys свяжите записи из таблиц, согласно таблице:

|ФИО|Заказ|
|------------|----|
|Иванов Иван Иванович| Книга |
|Петров Петр Петрович| Монитор |
|Иоганн Себастьян Бах| Гитара |

Приведите SQL-запросы для выполнения данных операций.

Приведите SQL-запрос для выдачи всех пользователей, которые совершили заказ, а также вывод данного запроса.
 
Подсказк - используйте директиву `UPDATE`.

### Ответ
```
# Приведите SQL-запросы для выполнения данных операций.
UPDATE clients SET заказ = 3 WHERE id = 1;
UPDATE clients SET заказ = 4 WHERE id = 2;
UPDATE clients SET заказ = 5 WHERE id = 3;

# Приведите SQL-запрос для выдачи всех пользователей, которые совершили заказ, а также вывод данного запроса.
test_db=> select * from clients where заказ > 0;
 id |       фамилия        | страна проживания | заказ
----+----------------------+-------------------+-------
  1 | Иванов Иван Иванович | USA               |     3
  2 | Петров Петр Петрович | Canada            |     4
  3 | Иоганн Себастьян Бах | Japan             |     5
(3 rows)
```
## Задача 5

Получите полную информацию по выполнению запроса выдачи всех пользователей из задачи 4 
(используя директиву EXPLAIN).

Приведите получившийся результат и объясните что значат полученные значения.

## Задача 6

Создайте бэкап БД test_db и поместите его в volume, предназначенный для бэкапов (см. Задачу 1).

Остановите контейнер с PostgreSQL (но не удаляйте volumes).

Поднимите новый пустой контейнер с PostgreSQL.

Восстановите БД test_db в новом контейнере.

Приведите список операций, который вы применяли для бэкапа данных и восстановления. 

