#include <bits/stdc++.h>
using namespace std;
int a[1000][1000];
int rr[1000];
int cc[1000];
int main() {
  int n, m, k;
  scanf("%d%d%d", &n, &m, &k);
  for (int i = 0; i < n; ++i) {
    rr[i] = i;
  }
  for (int i = 0; i < m; ++i) {
    cc[i] = i;
  }
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
      scanf("%d", &a[i][j]);
    }
  }
  for (int i = 0; i < k; ++i) {
    char c[2];
    int x, y;
    scanf("%s %d %d", c, &x, &y);
    if (c[0] == 'r') {
      swap(rr[x - 1], rr[y - 1]);
    } else if (c[0] == 'c') {
      swap(cc[x - 1], cc[y - 1]);
    } else if (c[0] == 'g') {
      printf("%d\n", a[rr[x - 1]][cc[y - 1]]);
    }
  }
}
