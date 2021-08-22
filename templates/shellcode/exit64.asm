[SECTION .text]
global _start

_start:
    xor     rdi, rdi
    mov      al, 0x3c
    cdq
    syscall
