#!/usr/bin/env python3

import socket

domains = {'google.com':'108.177.14.139', 'mail.google.com':'173.194.220.18', 'drive.google.com':'173.194.73.194'}

for domain in domains:
  ip = socket.gethostbyname(domain)
  if ip == domains[domain]:
    print(domain + ' - ' + domains[domain])
  else:
    print ('[ERROR] ' + domain + ' IP mismatch: ' + domains[domain] + ' ' + ip)
exit()

