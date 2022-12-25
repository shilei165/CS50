#include <cs50.h>
#include <stdio.h>

int main (void)
{
    long cardnumber = get_long("Card Number: ");

    // Total digit numbers
    int i = 0;
    long temp = cardnumber;
    while (temp > 0)
    {
        int digit = temp % 10;
        i = i + 1;
        temp = temp / 10;
        printf("digit: %i\n",digit);
    }

    printf("total card number: %i\n", i);

    // First two digits
    long start_2 = cardnumber;
    if (i % 2 == 0)
    {
        do
        {
            start_2 = start_2 / 100;
        }
        while (start_2 > 100);
        printf("The first two digits: %li\n", start_2);
    }
    else
    {
        start_2 = cardnumber / 10;
        do
        {
            start_2 = start_2 / 100;
        }
        while (start_2 > 100);
        printf("The first two digits: %li\n", start_2);
    }

    // First digit
    long start_1 = cardnumber;
    while (start_1 > 10)
    {
        start_1 = start_1 / 10;
    }
    printf("The first digit: %li\n", start_1);

    if (i == 15 && (start_2 == 34 || start_2 == 37))
    {
            printf("AMEX\n");
    }

    else if (i == 16 && (start_2 > 50 && start_2 < 56))
    {
        printf("MASTERCARD\n");
    }

    else if ((i == 16 || i == 13) && start_1 == 4)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }

}