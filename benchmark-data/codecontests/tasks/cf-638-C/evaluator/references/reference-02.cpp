#include <bits/stdc++.h>
using namespace std;
template <class T>
inline void rread(T& num) {
  num = 0;
  T f = 1;
  char ch = getchar();
  while (ch < '0' || ch > '9') {
    if (ch == '-') f = -1;
    ch = getchar();
  }
  while (ch >= '0' && ch <= '9') num = num * 10 + ch - '0', ch = getchar();
  num *= f;
}
inline int getgcd(int x, int y) {
  if (!x) return y;
  return getgcd(y % x, x);
}
inline long long getlcm(int x, int y) {
  return (long long)x / getgcd(x, y) * y;
}
inline long long getgcd(long long x, long long y) {
  if (!x) return y;
  return getgcd(y % x, x);
}
inline long long getlcm(long long x, long long y) {
  return x / getgcd(x, y) * y;
}
inline int power(int x, int k, int p) {
  int res = 1;
  while (k) {
    if (k & 1) res = (long long)res * x % p;
    x = (long long)x * x % p;
    k >>= 1;
  }
  return res;
}
const int maxn = 500005;
int tot, n, ans;
int head[maxn], des[maxn << 1], nxt[maxn << 1];
int fa[maxn], d[maxn], x[maxn], y[maxn], belong[maxn], id1[maxn], id2[maxn];
bool vis[maxn];
inline void adde(int x, int y) {
  des[++tot] = y;
  nxt[tot] = head[x];
  head[x] = tot;
}
inline void dfs(int x, int fa, int preb) {
  int now = 0;
  for (int(p) = head[(x)]; (p); (p) = nxt[(p)])
    if (des[p] != fa) {
      now++;
      if (now == preb) now++;
      belong[p] = belong[p ^ 1] = now;
      dfs(des[p], x, now);
    }
}
vector<int> ans2[maxn];
inline void judge() {
  freopen("data.in", "r", stdin);
  freopen("data.out", "w", stdout);
}
int main() {
  rread(n);
  tot = 1;
  for (int(i) = (1); (i) <= (n - 1); (i)++) {
    rread(x[i]);
    rread(y[i]);
    adde(x[i], y[i]);
    id1[i] = tot;
    adde(y[i], x[i]);
    id2[i] = tot;
    d[x[i]]++;
    d[y[i]]++;
  }
  for (int(i) = (1); (i) <= (n); (i)++) ans = max(ans, d[i]);
  printf("%d\n", ans);
  dfs(1, 0, 0);
  for (int(i) = (1); (i) <= (n - 1); (i)++) ans2[belong[id1[i]]].push_back(i);
  for (int(i) = (1); (i) <= (ans); (i)++) {
    printf("%d ", ans2[i].size());
    for (int(j) = (0); (j) < (ans2[i].size()); (j)++) printf("%d ", ans2[i][j]);
    puts("");
  }
  return 0;
}
