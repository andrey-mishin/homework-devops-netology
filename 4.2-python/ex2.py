#!/usr/bin/env python3

import os

bash_command = ["cd ~/.git/test-repo", "git status", "pwd"]
result_os = os.popen(' && '.join(bash_command)).read()
pwd = result_os.split('\n')
print("Local repository is:", pwd[-2])
for result in result_os.split('\n'):				
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', 'modified file: ') 
       	print(prepare_result)
