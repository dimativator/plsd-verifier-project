#include <bits/stdc++.h>
using namespace std;
inline long long read() {
  long long f = 1, ans = 0;
  char c = getchar();
  while (c < '0' || c > '9') {
    if (c == '-') f = -1;
    c = getchar();
  }
  while (c >= '0' && c <= '9') {
    ans = ans * 10 + c - '0';
    c = getchar();
  }
  return f * ans;
}
const long long MAXN = 1e5 + 11;
long long N, rt, siz[MAXN], Ans;
vector<long long> vec[MAXN];
void dfs(long long u, long long fath, long long opt) {
  long long Maxn = 0;
  siz[u] = 1;
  for (auto v : vec[u]) {
    if (v == fath) continue;
    dfs(v, u, opt);
    siz[u] += siz[v];
    Maxn = max(Maxn, siz[v]);
  }
  Maxn = max(Maxn, N - siz[u]);
  if (!opt)
    if (!Ans || Maxn < Ans) Ans = Maxn, rt = u;
  return;
}
long long sta[MAXN], nex[MAXN];
void dfs1(long long u, long long fath) {
  sta[++sta[0]] = u;
  for (auto v : vec[u])
    if (v != fath) dfs1(v, u);
}
signed main() {
  N = read();
  for (long long i = 1; i < N; i++) {
    long long u = read(), v = read();
    vec[u].push_back(v), vec[v].push_back(u);
  }
  dfs(1, 0, 0);
  dfs(rt, 0, 1);
  long long Ans = 0;
  for (long long i = 1; i <= N; i++) Ans += 2 * min(siz[i], N - siz[i]);
  printf("%lld\n", Ans);
  for (auto u : vec[rt]) dfs1(u, rt);
  sta[++sta[0]] = rt;
  long long e = (N / 2);
  for (long long i = 1; i <= e; i++) {
    long long u = sta[i], v = sta[i + e];
    nex[u] = v, nex[v] = u;
  }
  if (N & 1) {
    long long u = sta[1], v = sta[1 + e], x = rt;
    nex[u] = v, nex[v] = rt, nex[rt] = u;
  }
  for (long long i = 1; i <= N; i++) printf("%lld ", nex[i]);
  printf("\n");
  return 0;
}
