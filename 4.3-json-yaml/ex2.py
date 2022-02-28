#!/usr/bin/env python3

import socket
import json
import yaml

domains = {'google.com':'142.251.1.102', 'mail.google.com':'108.177.14.17', 'drive.google.com':'142.251.1.194'}

for domain in domains:
  ip = socket.gethostbyname(domain)
  if ip == domains[domain]:
    print(domain + ' - ' + domains[domain])
    with open('result.json', 'w') as jsn:
      jsn.write(json.dumps(domains, indent=2))
    with open('result.yml', 'w') as yml:
      yml.write(yaml.dump(domains, explicit_start=True))
  else:
    print ('[ERROR] ' + domain + ' IP mismatch: ' + domains[domain] + ' ' + ip)
    domains[domain] = ip
    with open('result.json', 'w') as jsn:
      jsn.write(json.dumps(domains, indent=2))
    with open('result.yml', 'w') as yml:
      yml.write(yaml.dump(domains, explicit_start=True))

