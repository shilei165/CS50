#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        // Prompt user to define the height
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);

    // draw the pyramides

    // draw from hight 1 to n
    for (int i = 0; i < n; i++)
    {
        int s, b;
        s = n - i - 1;
        b = n - s;

        // type the spaces on the left side
        for (int j = 0; j < s; j++)
        {
            printf(" ");
        }

        // type the # on the left side
        for (int k = 0; k < b; k++)
        {
            printf("#");
        }

        // type the middle space
        printf("  ");

        // type the # on the right side
        for (int k = 0; k < b; k++)
        {
            printf("#");
        }

        // go to the next lines
        printf("\n");
    }



}