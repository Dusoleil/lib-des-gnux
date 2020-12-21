#include <iostream>
#include <string>

/*
 * Read in all of stdin (should be piped from objdump), look for bytecode hex,
 * and print this code, escaped in a C-string literal, to stdout.
 *
 * EG output: "\x01\x02\x03\x04"
 */

int main()
{
    std::string tmp;
    unsigned int hex;

    std::cout << "\"";

    while (true)
    {
        std::cin >> tmp;

        if (std::cin.eof())
            break;

        if (tmp.size() == 2 &&
            tmp.find(":") == std::string::npos &&
            sscanf(tmp.c_str(), "%x", &hex) > 0)
            std::cout << "\\x" << tmp;
    }

    std::cout << "\"\n";
    return 0;
}
