/*
 * hexbin.c
 *
 * This program takes no arguments, it simply interprets its input as hex
 * and outputs bytes.
 */

#include <stdio.h>
#include <stdint.h>

int main()
{
    uint8_t b;
    char ip[3] = {0};

    while (1)
    {
        fread(ip, 1, 2, stdin);

        if (feof(stdin))
            break;

        sscanf(ip, "%hhx", &b);
        fwrite(&b, 1, 1, stdout);
    }

    return 0;
}
