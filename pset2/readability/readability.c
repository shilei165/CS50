#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");
    // printf("%s\n", text);
    int le_count = count_letters(text);
    // printf("%i letters\n", le_count);

    int wo_count = count_words(text);
    // printf("%i words\n", wo_count);

    int se_count = count_sentences(text);
    // printf("%i sentences\n", se_count);

    float L = (float)le_count / wo_count * 100.00;
    float S = (float)se_count / wo_count * 100.00;

    int index = round(0.0588 * L - 0.296 * S - 15.8);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }

}

int count_letters(string text)
{
    int len = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if ((text[i] >= 'a' && text[i] <= 'z') || (text[i] >= 'A' && text[i] <= 'Z'))
        {
            len = len + 1;
        }
    }
    return len;
}

int count_words(string text)
{
    int len = 1;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == ' ')
        {
            len = len + 1;
        }
    }
    return len;
}

int count_sentences(string text)
{
    int len = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            len = len + 1;
        }
    }
    return len;
}