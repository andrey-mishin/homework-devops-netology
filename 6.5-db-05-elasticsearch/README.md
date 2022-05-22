# Домашнее задание к занятию "6.5. Elasticsearch"

## Задача 1

В этом задании вы потренируетесь в:
- установке elasticsearch
- первоначальном конфигурировании elastcisearch
- запуске elasticsearch в docker

Используя докер образ [centos:7](https://hub.docker.com/_/centos) как базовый и 
[документацию по установке и запуску Elastcisearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html):

- составьте Dockerfile-манифест для elasticsearch
- соберите docker-образ и сделайте `push` в ваш docker.io репозиторий
- запустите контейнер из получившегося образа и выполните запрос пути `/` c хост-машины

Требования к `elasticsearch.yml`:
- данные `path` должны сохраняться в `/var/lib`
- имя ноды должно быть `netology_test`

В ответе приведите:
- текст Dockerfile манифеста
- ссылку на образ в репозитории dockerhub
- ответ `elasticsearch` на запрос пути `/` в json виде

Подсказки:
- возможно вам понадобится установка пакета perl-Digest-SHA для корректной работы пакета shasum
- при сетевых проблемах внимательно изучите кластерные и сетевые настройки в elasticsearch.yml
- при некоторых проблемах вам поможет docker директива ulimit
- elasticsearch в логах обычно описывает проблему и пути ее решения

Далее мы будем работать с данным экземпляром elasticsearch.

### Ответ
```
1. cat Dockerfile
FROM centos:centos7
COPY ./elasticsearch-8.2.0 /elasticsearch
RUN adduser elasticsearch -s /bin/sh && chown -R elasticsearch:elasticsearch /elasticsearch; \
    mkdir /var/lib/elasticsearch && chown elasticsearch:elasticsearch /var/lib/elasticsearch
VOLUME /elasticsearch/config
USER elasticsearch
WORKDIR /elasticsearch/bin
ENTRYPOINT ./elasticsearch

2. https://hub.docker.com/layers/andreymishin/netology/centos7-es/images/sha256-e34128ea06b7499136a223adff29e1ef8ce02d4216f8115702f27b4bcf7669b0?context=explore

3. curl -u elastic http://localhost:9200/
Enter host password for user 'elastic':
{
  "name" : "netology_test",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "_na_",
  "version" : {
    "number" : "8.2.0",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "b174af62e8dd9f4ac4d25875e9381ffe2b9282c5",
    "build_date" : "2022-04-20T10:35:10.180408517Z",
    "build_snapshot" : false,
    "lucene_version" : "9.1.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}
```

## Задача 2

В этом задании вы научитесь:
- создавать и удалять индексы
- изучать состояние кластера
- обосновывать причину деградации доступности данных

Ознакомтесь с [документацией](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html) 
и добавьте в `elasticsearch` 3 индекса, в соответствии со таблицей:

| Имя | Количество реплик | Количество шард |
|-----|-------------------|-----------------|
| ind-1| 0 | 1 |
| ind-2 | 1 | 2 |
| ind-3 | 2 | 4 |

Получите список индексов и их статусов, используя API и **приведите в ответе** на задание.

Получите состояние кластера `elasticsearch`, используя API.

Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?

Удалите все индексы.

**Важно**

При проектировании кластера elasticsearch нужно корректно рассчитывать количество реплик и шард,
иначе возможна потеря данных индексов, вплоть до полной, при деградации системы.

### Ответ
```
1. список и состояние индексов:

curl -X GET http://localhost:9200/_cat/indices?v
health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   ind-1 YaYV0zraS3ObRzY4T_GgVQ   1   0          0            0       225b           225b
yellow open   ind-3 R9up5OFfT76DSht55M-62w   4   2          0            0       900b           900b
yellow open   ind-2 Iqrmv8WSRI6w7cR2cHh_tQ   2   1          0            0       450b           450b

2. состояние кластера ES:

curl -X GET http://localhost:9200/_cluster/health?pretty
{
  "cluster_name" : "elasticsearch",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 8,
  "active_shards" : 8,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 10,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 44.44444444444444
}

3. Индексы ind-2/3 находятся в состоянии yellow, т.к. эти индексы сконфигурены с наличием реплик, которые 
должны располагаться на другой ноде, но мой кластер состоит только из одной ноды.
Из-за того, что часть шардов в статусе UNASSIGNED весь кластер имеет состояние yellow.
```
## Задача 3

В данном задании вы научитесь:
- создавать бэкапы данных
- восстанавливать индексы из бэкапов

Создайте директорию `{путь до корневой директории с elasticsearch в образе}/snapshots`.

Используя API [зарегистрируйте](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-register-repository.html#snapshots-register-repository) 
данную директорию как `snapshot repository` c именем `netology_backup`.

**Приведите в ответе** запрос API и результат вызова API для создания репозитория.

Создайте индекс `test` с 0 реплик и 1 шардом и **приведите в ответе** список индексов.

[Создайте `snapshot`](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-take-snapshot.html) 
состояния кластера `elasticsearch`.

**Приведите в ответе** список файлов в директории со `snapshot`ами.

Удалите индекс `test` и создайте индекс `test-2`. **Приведите в ответе** список индексов.

[Восстановите](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-restore-snapshot.html) состояние
кластера `elasticsearch` из `snapshot`, созданного ранее. 

**Приведите в ответе** запрос к API восстановления и итоговый список индексов.

Подсказки:
- возможно вам понадобится доработать `elasticsearch.yml` в части директивы `path.repo` и перезапустить `elasticsearch`

### Ответ
```
1. Регистрация директории для snapshot:

curl -X PUT "localhost:9200/_snapshot/netology_backup?pretty" -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "/elasticsearch/snapshots"
  }
}
'
{
  "acknowledged" : true
}

2. Создан индекс test

curl -X GET http://localhost:9200/_cat/indices?v
health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test  iQptQVLTSsGbwv9sPqKIqA   1   0          0            0       225b           225b

3. Cписок файлов в директории со snapshot-ами:

sudo docker exec -it c7-es /bin/bash
[elasticsearch@d3ef1b40dd04 bin]$ ll ../snapshots/
total 36
-rw-r--r-- 1 elasticsearch elasticsearch   850 May 22 15:59 index-0
-rw-r--r-- 1 elasticsearch elasticsearch     8 May 22 15:59 index.latest
drwxr-xr-x 4 elasticsearch elasticsearch  4096 May 22 15:59 indices
-rw-r--r-- 1 elasticsearch elasticsearch 18310 May 22 15:59 meta-zGNWea_TQmCcafezCUXKeQ.dat
-rw-r--r-- 1 elasticsearch elasticsearch   357 May 22 15:59 snap-zGNWea_TQmCcafezCUXKeQ.dat

4. Список индексов после удаления test и создания test-2:

curl -X GET http://localhost:9200/_cat/indices?v
health status index  uuid                   pri rep docs.count docs.deleted store.size pri.store.size
yellow open   test-2 85USm4qLSgySvdLIpk7BmQ   1   1          0            0       225b           225b

5. Запрос к API восстановления и итоговый список индексов:

curl -X POST http://localhost:9200/_snapshot/netology_backup/snapshot-22052201/_restore?pretty

curl -X GET http://localhost:9200/_cat/indices?v
health status index  uuid                   pri rep docs.count docs.deleted store.size pri.store.size
yellow open   test-2 85USm4qLSgySvdLIpk7BmQ   1   1          0            0       225b           225b
green  open   test   emfG5dC3S-ScF2tmzQ57bw   1   0          0            0       225b           225b
```
