/* Just figuring out how some file i/o functions work.
 * The end goal is to write something similar to nextInt() from Java. */

 #include <stdio.h>

 int main(int argc, char **argv)
 {
	int i;
	FILE *fp;

	/* Read from file if filename provided, else from stdin. */
	if (argc > 1)
	{
		fp = fopen(argv[1], "r");
		if (fp == NULL)
		{
			printf("Error opening %s.\n", argv[1]);
			return(1);
		}
	} else
	{
		fp = stdin;
	}

	while (fscanf(fp, "%d", &i) == 1)
	{
		printf("Read number: %d\n", i);
	}

	return 0;
 }
