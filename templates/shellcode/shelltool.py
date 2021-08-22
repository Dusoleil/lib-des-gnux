#!/usr/bin/env python

# This script will convert shellcode disassembly into an escaped string literal
# and warn about problematic bytes in the payload.
#     objdump -d elf | ./shelltool.py

import sys

name = None
bytecode = []
badchars = [ 0x00, 0x0a ]

for line in sys.stdin:
    for tok in line.split():
        if name is None:
            name = tok
        if len(tok) == 2:
            try:
                bytecode.append(int(tok, base=16))
            except:
                pass

result = ''.join([ "\\x%02x"%(x) for x in bytecode ])
result = f'{name}"{result}"'

for x in badchars:
    if x in bytecode:
        result += f'    **0x{"%02x"%(x)} detected**'

print(result)
