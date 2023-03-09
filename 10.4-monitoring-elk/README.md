# Домашнее задание к занятию "10.04. ELK"

## Задание 1

Вам необходимо поднять в докере:
- elasticsearch(hot и warm ноды)
- logstash
- kibana
- filebeat

и связать их между собой.

Logstash следует сконфигурировать для приёма по tcp json сообщений.

Filebeat следует сконфигурировать для отправки логов docker вашей системы в logstash.

В директории [help](./help) находится манифест docker-compose и конфигурации filebeat/logstash для быстрого
выполнения данного задания.

Результатом выполнения данного задания должны быть:
- скриншот `docker ps` через 5 минут после старта всех контейнеров (их должно быть 5)
- скриншот интерфейса kibana

## Выполнение

Воспользовался директорией `help`.  

Проблему с `vm.max_map_count` решил следующим образом:
```
sudo sysctl vm.max_map_count=262144 
vm.max_map_count = 262144
```

После чего перестали отваливаться контейнеры `es-hot` и `es-warm`.  

Добавил настройку `json` фильтра в файле `logstash.conf`:
```
input {
  tcp {
    port => 5046
    codec => json
  }
}

filter {
  json {
    source => "message"
  }
}

output {
  elasticsearch {
    hosts => ["es-hot:9200"]
    index => "logstash-%{[@metadata][indexDate]}"
  }
  stdout { codec => rubydebug }
}
```
Для доступа к каждому сервису по доменному имени добавил строчку в `/etc/hosts`:
```
127.0.0.1	es-hot es-warm kibana logstash
```

[Скриншот `docker ps`](./files/docker-ps.png "docker ps") через 5 минут после старта всех контейнеров:
![Docket screenshot](./files/docker-ps.png)  
  
Правда, контейнеров уже 6 - 5 контейнеров с сервисами и 1 с приложением, которое генерит логи.


[Скриншот `kibana`](./files/kibana.png):
![Kibana screenshot](./files/kibana.png)

