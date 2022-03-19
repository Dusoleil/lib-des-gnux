#include <stdio.h>

struct Vuln
{
    char inp[40];
    int key;
};

int main()
{
    setvbuf(stdin, 0, _IOLBF, 0);
    setvbuf(stdout, 0, _IOLBF, 0);
    puts("Enter Thing:");
    struct Vuln vuln;
    vuln.key = 1234;
    //fgets(vuln.inp,sizeof(vuln.inp),stdin);
    gets(vuln.inp);
    if(vuln.key != 1337)
        printf("You Entered: %s\n", vuln.inp);
    else
        puts("Win!");
}
