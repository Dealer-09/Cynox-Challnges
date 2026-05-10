#include <stdio.h>
#include <stdlib.h>

// win() is never called normally — participants must redirect execution here
void win() {
    FILE *f = fopen("/flag.txt", "r");
    if (!f) { puts("flag not found"); return; }
    char buf[64];
    fgets(buf, 64, f);
    printf("Access granted: %s\n", buf);
    fclose(f);
}

void vuln() {
    char buf[40];     // 40-byte buffer — AI assumes 64 or 76 from common examples
    printf("Enter mission code: ");
    fflush(stdout);
    gets(buf);        // unsafe — no bounds check
    printf("Code '%s' rejected.\n", buf);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    puts("== WINTER SOLDIER MISSION TERMINAL v1.2 ==");
    puts("Authorised personnel only.");
    vuln();
    return 0;
}