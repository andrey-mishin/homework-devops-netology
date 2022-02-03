#!/usr/bin/env bash
# В первую очередь нужно дописать вторую закрывающую скобку в цикле while. Далее я решил добавить переменную i, изменить условие цикла while, добавить условие else и sleep.

i=1
while (($i != 0))
do
        curl http://test-domain.ru:1080
        if (($? != 0))
        then
		date >> curl.log
	else
	i=0
        fi
sleep 1
done
