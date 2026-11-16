#include <bits/stdc++.h>
using namespace std;
const int inf = 0x3f3f3f3f;
const int N = 107;
int mp[N][N];
int main() {
  int t, n;
  scanf("%d", &t);
  while (t--) {
    scanf("%d", &n);
    int x = 0, y = 1, z = 2;
    for (int i = 1; i <= n; ++i) {
      for (int j = 1; j <= n; ++j) {
        if (j > 1) printf(" ");
        if (j == x || j == y || j == z)
          printf("1");
        else
          printf("0");
      }
      printf("\n");
      x++, y++, z++;
    }
  }
  return 0;
}
