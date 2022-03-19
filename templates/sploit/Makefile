all: valoverwrite.elf ret2win.elf leakaddr.elf leakcanary.elf shellcode.elf ret2libc.elf

valoverwrite.elf: valoverwrite.c
	gcc valoverwrite.c -D_FORTIFY_SOURCE=0 -fno-stack-protector -o valoverwrite.elf

ret2win.elf: ret2win.c
	gcc ret2win.c -D_FORTIFY_SOURCE=0 -fno-stack-protector -fno-pie -no-pie -o ret2win.elf

leakaddr.elf: leakaddr.c
	gcc leakaddr.c -D_FORTIFY_SOURCE=0 -fno-stack-protector -o leakaddr.elf

leakcanary.elf: leakcanary.c
	gcc leakcanary.c -D_FORTIFY_SOURCE=0 -o leakcanary.elf

shellcode.elf: shellcode.c
	gcc shellcode.c -D_FORTIFY_SOURCE=0 -z execstack -o shellcode.elf

ret2libc.elf: ret2libc.c
	gcc ret2libc.c -D_FORTIFY_SOURCE=0 -o ret2libc.elf
