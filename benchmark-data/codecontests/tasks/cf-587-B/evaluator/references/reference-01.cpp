#include <bits/stdc++.h>
using namespace std;
const int maxn = 2000000;
const int mod = 1e9 + 7;
int n, k;
int get(int i, int j) { return (i - 1) * n + j; }
long long l;
int b[maxn], f[maxn], sum[maxn], a[maxn];
int ans = 0;
pair<int, int> c[maxn];
int main() {
  scanf("%d %I64d %d", &n, &l, &k);
  for (int i = 1; i <= n; i++) scanf("%d", &a[i]), c[i] = make_pair(a[i], i);
  sort(c + 1, c + 1 + n);
  for (int i = 1; i <= n; i++) b[i] = c[i].first;
  int cur = 0;
  if (1LL * n >= l)
    printf("%I64d\n", l);
  else {
    for (int i = 1; i <= n; i++) f[i] = 1, sum[i] = i;
    for (int i = 2; i <= k; i++) {
      for (int j = 1; j <= n; j++) {
        int tmp = (int)(upper_bound(b + 1, b + 1 + n, a[j]) - b - 1);
        if (tmp) f[get(i, j)] = sum[get(i - 1, tmp)];
      }
      for (int j = 1; j <= n; j++) {
        if (j == 1)
          sum[get(i, 1)] = f[get(i, c[j].second)];
        else
          sum[get(i, j)] = sum[get(i, j - 1)] + f[get(i, c[j].second)];
        if (sum[get(i, j)] >= mod) sum[get(i, j)] -= mod;
      }
    }
    long long size = l / n;
    int res = (int)(l % n);
    for (int i = 1; i <= min(1LL * k, size + 1); i++) {
      ans += 1LL * sum[get(i, n)] * ((size - i + 1) % mod) % mod;
      if (ans >= mod) ans -= mod;
      for (int j = 1; j <= res; j++) {
        int tmp = (int)(upper_bound(b + 1, b + 1 + n, a[j]) - b - 1);
        if (tmp) {
          ans += sum[get(i - 1, tmp)];
          if (ans >= mod) ans -= mod;
        }
      }
    }
    ans += res;
    if (ans >= mod) ans -= mod;
    printf("%d\n", ans);
  }
  return 0;
}
