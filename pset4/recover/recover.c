#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // check the arguments
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover IMAGE\n");
        return 1;
    }

    // open the file
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 2;
    }

    const int BLOCK_SIZE = 512;
    unsigned char buffer[BLOCK_SIZE];

    // pointer to outfile
    FILE *img = NULL;

    // leave space for jpg file name
    char image[8];

    // number of image files created
    int n = 0;

    // search until jep is found
    while (fread(buffer, BLOCK_SIZE, 1, file) == 1)
    {
        //find the begining of a jpg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // close image file if one has been created
            if (n > 0)
            {
                fclose(img);
            }
            // make name for nth image
            sprintf(image, "%03d.jpg", n);

            // open nth jpg file
            img = fopen(image, "w");
            if (img == NULL)
            {
                fprintf(stderr, "Could not create %s.\n", image);
                return 3;
            }
            n++;
        }

        // write to image file only if one exists
        if (img != NULL)
        {
            // write to image file
            fwrite(buffer, BLOCK_SIZE, 1, img);
        }
    }
    // close last image file
    fclose(img);

    // close card.raw
    fclose(file);

    return 0;
}