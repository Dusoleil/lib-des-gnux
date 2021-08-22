[SECTION .text]
global _start

_start:
    xor     ebx, ebx
    xor     eax, eax
    mov      al, 0x1
    int     0x80
