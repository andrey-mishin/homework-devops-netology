# Домашнее задание к занятию "6.4. PostgreSQL"

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.

Подключитесь к БД PostgreSQL используя `psql`.

Воспользуйтесь командой `\?` для вывода подсказки по имеющимся в `psql` управляющим командам.

**Найдите и приведите** управляющие команды для:
- вывода списка БД
- подключения к БД
- вывода списка таблиц
- вывода описания содержимого таблиц
- выхода из psql

### Ответ
```
1. вывода списка БД - \l
2. подключения к БД - \c [db-name] [user-name]
3. вывода списка таблиц - \d
4. вывода описания содержимого таблиц - \d [table-name]
5. выхода из psql - \q
```

## Задача 2

Используя `psql` создайте БД `test_database`.

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-04-postgresql/test_data).

Восстановите бэкап БД в `test_database`.

Перейдите в управляющую консоль `psql` внутри контейнера.

Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.

Используя таблицу [pg_stats](https://postgrespro.ru/docs/postgresql/12/view-pg-stats), найдите столбец таблицы `orders` 
с наибольшим средним значением размера элементов в байтах.

**Приведите в ответе** команду, которую вы использовали для вычисления и полученный результат.

### Ответ
```
test_database=# SELECT attname, avg_width FROM pg_stats WHERE tablename = 'orders';
 attname | avg_width
---------+-----------
 id      |         4
 title   |        16    # столбец с наибольшим средним значением размера элементов в байтах
 price   |         4
(3 rows)
```
## Задача 3

Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и
поиск по ней занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили
провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).

Предложите SQL-транзакцию для проведения данной операции.

Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?

### Ответ
```
# Транзакция 

BEGIN;
CREATE TABLE orders_1 (CHECK ( price > 499 ) ) INHERITS (orders);
ALTER TABLE ONLY public.orders_1 ADD CONSTRAINT orders_1_pkey PRIMARY KEY (id);
CREATE TABLE orders_2 (CHECK ( price <= 499 ) ) INHERITS (orders);
ALTER TABLE ONLY public.orders_2 ADD CONSTRAINT orders_2_pkey PRIMARY KEY (id);
COMMIT;
```
```
# Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?

Думаю, что нет. Если исходить из наших условий (таблица с 3 столбцами и разделение таблицы
по цене), то изначально нам не может быть известно какая цена на товары может быть в будущем
и до каких размеров таблица разрастётся.
К тому же, изначально нужно было бы вручную создавать две таблицы с некими условиями, которые на
момент создания исходной таблицы неизвестны.
```
## Задача 4

Используя утилиту `pg_dump` создайте бекап БД `test_database`.

Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца `title` для таблиц `test_database`?

# Ответ
```
# Добавить в строку создания таблицы orders UNIQUE чтобы строка в итоге выглядела так:

CREATE TABLE public.orders (
    id integer NOT NULL,
    title character varying(80) NOT NULL UNIQUE,
    price integer DEFAULT 0
);

# Добавить строки с ограничениями на таблицы orders_1 и orders_2:

ALTER TABLE ONLY public.orders_1 ADD CONSTRAINT orders_1_title_uniq UNIQUE (title);

ALTER TABLE ONLY public.orders_2 ADD CONSTRAINT orders_2_title_uniq UNIQUE (title);
```
