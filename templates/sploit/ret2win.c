#include <stdio.h>

void win()
{
    puts("Win!");
}

int main()
{
    setvbuf(stdin, 0, _IOLBF, 0);
    setvbuf(stdout, 0, _IOLBF, 0);
    puts("Enter Thing:");
    char inp[40];
    //fgets(inp,sizeof(inp),stdin);
    gets(inp);
    printf("You Entered: %s\n", inp);
}
