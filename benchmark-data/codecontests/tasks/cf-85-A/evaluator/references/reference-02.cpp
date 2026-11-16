#include <bits/stdc++.h>
int main() {
  int n;
  scanf("%d", &n);
  if (n & 1) {
    int l = (n - 1) / 2;
    printf("a");
    for (int i = 0; i < l; i++) printf(i & 1 ? "bb" : "cc");
    puts("");
    printf("a");
    for (int i = 0; i < l; i++) printf(!(i & 1) ? "bb" : "cc");
    puts("");
    for (int i = 0; i < l; i++) printf(i & 1 ? "dd" : "ee");
    printf("f");
    puts("");
    for (int i = 0; i < l; i++) printf(!(i & 1) ? "dd" : "ee");
    printf("f");
    puts("");
  } else {
    int l = n / 2;
    for (int i = 0; i < l; i++) printf(i & 1 ? "bb" : "aa");
    puts("");
    putchar('b');
    for (int i = 0; i < l - 1; i++) printf(i & 1 ? "cc" : "dd");
    putchar('f');
    puts("");
    putchar('b');
    for (int i = 0; i < l - 1; i++) printf(!(i & 1) ? "cc" : "dd");
    putchar('f');
    puts("");
    for (int i = 0; i < l; i++) printf(i & 1 ? "aa" : "ee");
    puts("");
  }
  return 0;
}
