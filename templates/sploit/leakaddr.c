#include <stdio.h>
#include <unistd.h>
#include <string.h>

void win()
{
    puts("Win!");
}

void vuln()
{
    puts("Enter Thing:");
    char inp[40] = {0};
    //fgets(inp,sizeof(inp),stdin);
    read(STDIN_FILENO, inp, 100);
    printf("You Entered: %s\n", inp);
    memset(inp, 0, 40);
    puts("Enter Thing:");
    //fgets(inp,sizeof(inp),stdin);
    read(STDIN_FILENO, inp, 100);
    printf("You Entered: %s\n", inp);
}

int main()
{
    setvbuf(stdin, 0, _IOLBF, 0);
    setvbuf(stdout, 0, _IOLBF, 0);
    vuln();
}
