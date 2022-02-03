#!/usr/bin/env bash

a=1
array_ip=(192.168.0.1 173.194.222.113 87.250.250.242)
while (($a < 6))
do
	for i in ${array_ip[@]}
	do
	curl -s $i:80 1>/dev/null
		if (($? != 0))
			then
			echo "`date "+%D %T"` | check #$a: $i:80 is not available" >> check_ip.log
			else
			echo "`date "+%D %T"` | check #$a: $i:80 is available" >> check_ip.log
		fi
	sleep 1
	done
let "a+=1"
done
