/* Just figuring out how some file i/o functions work.
 * The end goal is to write something similar to nextInt() from Java. */

 #include <stdio.h>

 int main()
 {
	int i;

	while (scanf("%d", &i) == 1)
	{
		printf("Read number: %d\n", i);
	}

	return 0;
 }
