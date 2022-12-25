#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int is_digit(string arg);

int main(int argc, string argv[])
{
    string arg = argv[1];
    if (argc == 2 && is_digit(arg)) // check there is only 1 digit argument
    {
        int k = atoi(argv[1]);

        string plaintext = get_string("plaintext:  ");
        printf("ciphertext:  ");

        // iterate through plain text letter by letter
        for (int i = 0, n = strlen(plaintext); i < n; i++)
        {
            char p = plaintext[i];
            if (p >= 'a' && p <= 'z')
            {
                char c = (p - 'a' + k) % 26 + 'a';
                printf("%c", c);
            }
            else if (p >= 'A' && p <= 'Z')
            {
                char c = (p - 'A' + k) % 26 + 'A';
                printf("%c", c);
            }
            else
            {
                printf("%c", p);
            }

        }

        printf("\n");
        return 0;

    }

    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
}

// check if the arguments are digits
int is_digit(string arg)
{
    for (int i = 0, n = strlen(arg); i < n; i++)
    {
        char s = arg[i];
        if (!isdigit(s))
        {
            return 0;
        }
    }
    return 1;
}