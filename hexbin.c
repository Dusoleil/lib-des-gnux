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

    while (1)
    {
        scanf("%hhx", &b);
        if (feof(stdin))
            break;
        fwrite(&b, 1, 1, stdout);
    }

    return 0;
}
