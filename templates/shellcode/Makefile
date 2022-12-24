LDFLAGS?=
FORMAT?=elf64
CODE?=examples/shell64.asm
GREP=00|0a

.PHONY: all elf disas

# Format bytecode as an escaped string, highlight bad bytes
all: code.bin
	@xxd -i -c 16 <code.bin \
		| sed 's/,//g;s/ 0/\\/g;s/^ */"/g;s/$$/"/g' \
		| grep --color=always -E '$(GREP)|$$'

elf: code.o
	ld $(LDFLAGS) code.o -o code.elf

disas: code.o
	@objdump -d code.o \
		| grep --color=always -E '$(GREP)|$$'

code.bin: code.o
	objcopy -O binary code.o code.bin

code.o: code.asm
	nasm -f '$(FORMAT)' code.asm -o code.o

code.asm:
	cp '$(CODE)' code.asm


# -melf_i386
