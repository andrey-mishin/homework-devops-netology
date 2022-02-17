#!/usr/bin/env python3

import os

bash_command = ["cd ~/.git/test-repo", "git status", "pwd"]
result_os = os.popen(' && '.join(bash_command)).read()
pwd = result_os.split('\n')[-2]
for result in result_os.split('\n'):				
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '') 
       	print(pwd + '/' + prepare_result)
