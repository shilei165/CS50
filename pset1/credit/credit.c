#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long n = get_long("Number: ");


// check if the card is valid by implementing Luhn's algorithm

    int sum_1 = 0;
    int sum_2 = 0;
    int sum = 0;
    int i = 1;

    long cardnumber = n;
    do
    {
        int digit = cardnumber % 10; 
        if (i % 2 != 0)
        {
            sum_1 = sum_1 + digit;
            //printf("odd digit: %i\n",digit);
        }
        else
        {
            int product = digit * 2;
            if (product < 10)
            {
                sum_2 = sum_2 + product;
            }
            else
            {
                sum_2 = sum_2 + product / 10 + product % 10;
            }
            //printf("even digit: %i\n",digit);
        }
        sum = sum_1 + sum_2;
        i = i + 1;
        cardnumber = cardnumber / 10;

    }
    while (cardnumber > 0);

    //printf("sum_1: %i\n",sum_1);
    //printf("sum_2: %i\n",sum_2);

    if (sum % 10 != 0)
    {
        printf("INVALID\n");
        //printf("The sum is %i\n",sum);
        return 0;
    }

// check card type

    // First two digits
    long start_2 = n;
    int j = i - 1;
    if (j % 2 == 0)
    {
        do
        {
            start_2 = start_2 / 100;
            //printf("The quotient: %li\n", start_2);
        }
        while (start_2 > 100);
        //printf("The first two digits: %li\n", start_2);
    }
    else
    {
        start_2 = n / 10;
        do
        {
            start_2 = start_2 / 100;
        }
        while (start_2 > 100);
        //printf("The first two digits: %li\n", start_2);
    }

    // First digit
    long start_1 = n;
    while (start_1 > 10)
    {
        start_1 = start_1 / 10;
    }
    //printf("The first digit: %li\n", start_1);

    if (j == 15 && (start_2 == 34 || start_2 == 37))
    {
        printf("AMEX\n");
    }

    else if (j == 16 && (start_2 > 50 && start_2 < 56))
    {
        printf("MASTERCARD\n");
    }

    else if ((j == 16 || j == 13) && start_1 == 4)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
    return 0;
}
