#include <bits/stdc++.h>
const int a[6][6] = {{0, 1, 1, 0, 1, 0}, {0, 0, 1, 1, 0, 1},
                     {0, 0, 0, 1, 1, 0}, {1, 0, 0, 0, 1, 1},
                     {0, 1, 0, 0, 0, 1}, {1, 0, 1, 0, 0, 0}};
const int b[3][3] = {
    {0, 1, 0},
    {0, 0, 1},
    {1, 0, 0},
};
int c[1000 + 9][1000 + 9], n;
int main() {
  int n;
  scanf("%d", &n);
  if (n == 4) return puts("-1");
  if (n % 2 == 0)
    for (int i = 0; i < 6; ++i)
      for (int j = 0; j < 6; ++j) c[i][j] = a[i][j];
  else
    for (int i = 0; i < 3; ++i)
      for (int j = 0; j < 3; ++j) c[i][j] = b[i][j];
  for (int i = (n % 2) ? 3 : 6; i < n; i += 2) {
    c[i][i + 1] = 1;
    for (int j = 0; j < i; ++j) c[j][i] = c[i + 1][j] = 1;
  }
  for (int i = 0; i < n; ++i)
    for (int j = 0; j < n; ++j)
      if (!c[i][j] && !c[j][i] && i != j) c[i][j] = 1;
  for (int i = 0; i < n; ++i, puts(""))
    for (int j = 0; j < n; ++j) printf("%d ", c[i][j]);
}
