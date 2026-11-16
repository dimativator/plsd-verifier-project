#include <bits/stdc++.h>
using namespace std;
inline long long read() {
  long long x = 0, f = 1;
  char c = getchar();
  while (c != '-' && (c < '0' || c > '9')) c = getchar();
  if (c == '-') f = -1, c = getchar();
  while (c >= '0' && c <= '9') x = x * 10 + c - '0', c = getchar();
  return f * x;
}
const long long N = 4e1 + 2;
const long long M = 1e9 + 7;
const long long MAXN = 2e18 + 7;
const long long Mod = 998244353;
long long _, i, j, k, n, m, p, q, s, T, t, l, r, o, u, v, w, x, y, z, ans, nex,
    sum, num, len, st, en, sx, sy, tx, ty, th, ma, mi, mod, op, res, flag, cas,
    bk, ret, mid, cnt, now, tmp, rt;
long long a[N], c[N], dp[N];
char ch;
vector<pair<long long, long long> > h;
string s1, s2, s3;
void dfs(long long l, long long r) {
  if (l == r) return;
  long long mid = (l + r) >> 1;
  dfs(l, mid);
  dfs(mid + 1, r);
  for (long long i = l; i <= mid; i++)
    h.push_back(pair<long long, long long>(i, mid + i - l + 1));
}
signed main() {
  long long T = 1;
  a[0] = 1;
  for (i = 1; i < 20; i++) a[i] = a[i - 1] << 1;
  while (T--) {
    n = read();
    p = 1;
    for (p = 1; a[p] < n; p++)
      ;
    p--;
    dfs(1, a[p]);
    dfs(n - a[p] + 1, n);
    printf("%lld\n", (long long)h.size());
    for (i = 0; i < h.size(); i++)
      printf("%lld %lld\n", h[i].first, h[i].second);
  }
  return 0;
}
