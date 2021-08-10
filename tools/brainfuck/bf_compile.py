#!/usr/bin/env python
import sys

if len(sys.argv) < 2:
    print("Give me filename...")
    exit()

bytecode = {
    '>': b"\x00",
    '<': b"\x02",
    '+': b"\x07",
    '-': b"\x06",
    '.': b"\x05",
    ',': b"\x04",
    '[': b"\x03",
    ']': b"\x01",
}

src_buff = open(sys.argv[1]).read()
bin_file = open(sys.argv[1]+".bin", mode="wb")

for c in src_buff:
    try:
        b = bytecode[c]
        bin_file.write(b)
    except KeyError:
        # Ignore whitespace, etc.
        pass

bin_file.close()
