#include <stdio.h>
#include <unistd.h>
#include <string.h>

void vuln()
{
    char inp[40] = {0};
    while(1)
    {
        puts("Menu:");
        puts("1 - Enter Thing");
        puts("2 - Quit");
        puts("Choice:");
        memset(inp, 0, 40);
        fgets(inp, sizeof(inp), stdin);
        if(!strcmp(inp, "1\n"))
        {
            puts("Enter Thing:");
            //fgets(inp,sizeof(inp),stdin);
            read(STDIN_FILENO, inp, 200);
            printf("You Entered: %s\n", inp);
        }
        else if(!strcmp(inp, "2\n"))
            break;
        else
            puts("Unknown Option!");
    }
}

int main()
{
    setvbuf(stdin, 0, _IOLBF, 0);
    setvbuf(stdout, 0, _IOLBF, 0);
    vuln();
}
