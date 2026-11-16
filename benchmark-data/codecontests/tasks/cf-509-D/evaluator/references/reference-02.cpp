#include <bits/stdc++.h>
using namespace std;
long long a[105], b[105], w[105][105], e[105][105];
long long gcd(long long a, long long b) { return b ? gcd(b, a % b) : a; }
void ok(int n, int m, long long k) {
  printf("YES\n%I64d\n", k);
  for (int i = 1; i <= n; i++) printf("%I64d%c", a[i] % k + k, " \n"[i == n]);
  for (int i = 1; i <= m; i++) printf("%I64d%c", b[i] % k + k, " \n"[i == m]);
}
int main() {
  int n, m;
  scanf("%d%d", &n, &m);
  for (int i = 1; i <= n; i++)
    for (int j = 1; j <= m; j++) scanf("%I64d", &w[i][j]);
  for (int j = 1; j <= m; j++) b[j] = w[1][j];
  for (int i = 1; i <= n; i++) a[i] = w[i][1] - w[1][1];
  long long mx = 0;
  for (int i = 1; i <= n; i++)
    for (int j = 1; j <= m; j++)
      mx = max(mx, e[i][j] = abs(a[i] + b[j] - w[i][j]));
  if (!mx) {
    long long k = 0;
    for (int i = 1; i <= n; i++)
      for (int j = 1; j <= m; j++) k = max(k, w[i][j] + 1);
    ok(n, m, k);
  } else {
    for (int i = 1; i <= n; i++)
      for (int j = 1; j <= m; j++) mx = gcd(mx, e[i][j]);
    for (int i = 1; i <= n; i++)
      for (int j = 1; j <= m; j++)
        if (mx <= w[i][j]) return 0 * printf("NO");
    ok(n, m, mx);
  }
  return 0;
}
