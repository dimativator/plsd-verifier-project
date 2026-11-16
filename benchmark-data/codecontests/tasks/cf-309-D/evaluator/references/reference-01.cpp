#include <bits/stdc++.h>
using namespace std;
int n, m;
long long ans;
int main() {
  scanf("%d%d", &n, &m);
  for (int i = m + 1; i <= (n + 1) / 2; i++) {
    int p = n + 1 - i;
    int q = 2 * i;
    for (int j = m + 1; j <= n - m; j++) {
      int tmp = (p * (q - j) - 1) / (i + j);
      int now = (((tmp) < (n - m)) ? tmp : n - m);
      if (now <= m) break;
      ans += now - m;
    }
    if (i == n / 2) ans = ans * 2;
  }
  ans = ans * 3;
  printf("%I64d", ans);
  return 0;
}
