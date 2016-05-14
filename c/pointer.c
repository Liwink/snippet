#import <stdio.h>
#import <stdlib.h>

int pointer_const()
{
    const int c = 1;
    int x = 0;
    int *ip, *cp;
    ip = &x;
    printf("&c: %p\n", &c);
    printf("c: %d\n", c);
    printf("\n");
    cp = &c;
    *cp = 2;
    printf("*cp: %d\n", *cp);
    printf("cp: %p\n", cp);
    printf("c: %d\n", c);
    printf("*&c: %d\n", *&c);
    printf("&c: %p\n", &c);
    return 1;
}

void scpy(char *a, char *b)
{
    while (*(a++) = *(b++))
        ;
}

void pointer_string()
{
    char ames[] = "now";
    char *pmes = "now";

    printf("%s\n", ames);
    printf("%s\n", pmes);
    printf("%c\n", pmes[0]);

    char *mmes = malloc(256);
    scpy(mmes, pmes);
    printf("%s\n", mmes);

    *mmes = 'N';
    mmes[3] = '1';
    // mmes[4] = '\0';
    printf("%s\n", mmes);

    free(mmes);

    // *(pmes+1) = '0';
    // *(pmes+4) = '\0';
}

int
main(int argc, char *argv[])
{
    // pointer_string();
    int **ppi;
    int *pi;
    int i=99;
    pi = &i;
    ppi = &pi;
    printf("%d\n", **ppi);
    printf("%p\n", *ppi);
}
