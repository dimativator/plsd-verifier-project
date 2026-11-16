#include <bits/stdc++.h>
using namespace std;
int a[20];
int p;
long long dp[20][2525][50];
int b[2525];
long long gcd(long long m, long long n) {
  int maxx = max(m, n);
  int minn = min(m, n);
  if (minn == 0) return maxx;
  while (minn) {
    long long x = minn;
    minn = maxx % minn;
    maxx = x;
  }
  return m * n / maxx;
}
int cnt = 0;
long long dfs(long long pos, long long pre, long long GCD, int limit) {
  if (b[GCD] == 0) b[GCD] = ++cnt;
  if (pos <= 0) {
    if (GCD != 0) {
      if (pre % GCD == 0)
        return 1;
      else
        return 0;
    } else
      return 0;
  }
  if (!limit && dp[pos][pre][b[GCD]] != -1) return dp[pos][pre][b[GCD]];
  int n = limit ? a[pos] : 9;
  long long ans = 0;
  for (long long i = 0; i <= n; i++) {
    ans +=
        dfs(pos - 1, (pre * 10 + i) % 2520, gcd(i, GCD), limit && i == a[pos]);
  }
  if (!limit) dp[pos][pre][b[GCD]] = ans;
  return ans;
}
long long solve(long long x) {
  p = 1;
  memset(a, 0, sizeof(a));
  while (x > 0) {
    a[p] = x % 10;
    x /= 10;
    p++;
  }
  return dfs(p - 1, 0, 0, 1);
}
int main() {
  int T;
  scanf("%d", &T);
  long long n, m;
  memset(dp, -1, sizeof(dp));
  while (T--) {
    scanf("%I64d%I64d", &n, &m);
    printf("%I64d\n", solve(m) - solve(n - 1));
  }
  return 0;
}
