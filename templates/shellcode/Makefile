.PHONY: all

all: shell32.elf shell64.elf
	@objdump -d shell32.elf | ./shelltool.py
	@objdump -d shell64.elf | ./shelltool.py

shell32.o: shell32.asm
	nasm -f elf shell32.asm -o shell32.o

shell32.elf: shell32.o
	ld -melf_i386 shell32.o -o shell32.elf

shell64.o: shell64.asm
	nasm -f elf64 shell64.asm -o shell64.o

shell64.elf: shell64.o
	ld shell64.o -o shell64.elf
