#include <bits/stdc++.h>
using namespace std;
const int N = 3e3 + 4;
const int INF = 0x3f3f3f3f;
int n;
int a[N], b[N], pos[N];
bool ok[N][N];
inline int read() {
  int x = 0;
  char c = getchar();
  while (c < '0' || c > '9') c = getchar();
  while (c >= '0' && c <= '9') x = x * 10 + c - '0', c = getchar();
  return x;
}
inline void smax(int &x, int y) { x = x < y ? y : x; }
int main() {
  int kase = read();
  while (kase--) {
    n = read();
    for (int i = 1; i <= n; ++i) b[i] = a[i] = read();
    sort(b + 1, b + n + 1);
    for (int i = 1; i <= n; ++i) {
      a[i] = lower_bound(b + 1, b + n + 1, a[i]) - b;
      pos[a[i]] = i;
    }
    int len = 1;
    for (int i = 1; i <= n; ++i) ok[i][i] = true;
    for (int i = 1; i < n; ++i)
      for (int j = i + 1; j <= n; ++j) {
        ok[i][j] = (ok[i][j - 1] && pos[j] > pos[j - 1]);
        if (ok[i][j]) smax(len, j - i + 1);
      }
    printf("%d\n", n - len);
  }
  return 0;
}
