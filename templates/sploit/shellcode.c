#include <stdio.h>
#include <unistd.h>
#include <string.h>

void vuln()
{
    char inp[400] = {0};
    puts("Enter Thing:");
    //fgets(inp,sizeof(inp),stdin);
    read(STDIN_FILENO, inp, 430);
    printf("You Entered: %s\n", inp);
    memset(inp, 0, 400);
    puts("Enter Thing:");
    //fgets(inp,sizeof(inp),stdin);
    read(STDIN_FILENO, inp, 430);
    printf("You Entered: %s\n", inp);
}

int main()
{
    setvbuf(stdin, 0, _IOLBF, 0);
    setvbuf(stdout, 0, _IOLBF, 0);
    vuln();
}
