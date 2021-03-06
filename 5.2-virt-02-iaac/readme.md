# Домашнее задание к занятию "5.2. Применение принципов IaaC в работе с виртуальными машинами"

## Задача 1

- Опишите своими словами основные преимущества применения на практике IaaC паттернов.
- Какой из принципов IaaC является основополагающим?

## Ответ
```
- Снижение стоимости исправления дефектного кода, за счёт того, 
что место дефекта обнаруживается в максимально сжатые сроки.
- Основопологающий принцип IaaC - это идемпотентность. Создавая 
и редактируя некий шаблон можно создавать и изменять инфрастуктуру 
независимо от её размера. Изменения внесённые в одном месте автоматически 
распространятся на всю инфраструктуру.
```

## Задача 2

- Чем Ansible выгодно отличается от других систем управление конфигурациями?
- Какой, на ваш взгляд, метод работы систем конфигурации более надёжный push или pull?

## Ответ
```
- Ansible работает по SSH без необходимости использования агентов 
на конфигурируемых машинах.
- На мой взгляд метод Push более надёжный, т.к. агент, который должен 
запросить конфиг у управляющего сервера может зависнуть или не запуститься. 
Или например IP-адрес управляющего сервера изменился, но часть управляемых 
машин об этом не знает и не сможет получить обновления конфигов.
```

## Задача 3

Установить на личный компьютер:

- VirtualBox
- Vagrant
- Ansible

*Приложить вывод команд установленных версий каждой из программ, оформленный в markdown.

## Ответ

```console
baloo@pc:~$ vagrant --version
Vagrant 2.2.6
baloo@pc:~$ vboxmanage --version
6.1.26_Ubuntur145957
baloo@pc:~$ ansible --version
ansible 2.9.6
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/baloo/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  executable location = /usr/bin/ansible
  python version = 3.8.10 (default, Nov 26 2021, 20:14:08) [GCC 9.3.0]
```

