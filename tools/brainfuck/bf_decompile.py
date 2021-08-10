#!/usr/bin/env python
import sys

if len(sys.argv) < 2:
    print("Give me filename...")
    exit()

bytecode = {
    0: '>',
    2: '<',
    7: '+',
    6: '-',
    5: '.',
    4: ',',
    3: '[',
    1: ']',
}

bin_buff = open(sys.argv[1], mode="rb").read()
src_file = open(sys.argv[1]+".bf", mode="w")

for b in bin_buff:
    try:
        c = bytecode[b & 0x07]
        src_file.write(c)
    except:
        print("Error while processing file (aborting...)")
        exit()

src_file.close()
