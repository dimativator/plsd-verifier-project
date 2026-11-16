#include <bits/stdc++.h>
int val[200010], cnt, next[200010], head[200010], s[100010], ans[400010], out,
    n, m, st;
bool vis[100010];
void add(int a, int b) {
  val[++cnt] = b;
  next[cnt] = head[a];
  head[a] = cnt;
}
void work(int x) {
  s[x] ^= 1;
  ans[++out] = x;
}
void dfs(int u) {
  work(u);
  vis[u] = true;
  for (int i = head[u]; i; i = next[i]) {
    int v = val[i];
    if (vis[v]) continue;
    dfs(v);
    work(u);
    if (s[v]) {
      work(v);
      work(u);
    }
  }
}
int main() {
  scanf("%d%d", &n, &m);
  for (int i = 1; i <= m; i++) {
    int u, v;
    scanf("%d%d", &u, &v);
    add(u, v);
    add(v, u);
  }
  for (int i = 1; i <= n; i++) {
    scanf("%d", &s[i]);
    if (s[i] == 1) st = i;
  }
  dfs(st);
  if (s[st]) {
    s[st] = 0;
    out--;
  }
  for (int i = 1; i <= n; i++)
    if (s[i] != 0) {
      printf("-1\n");
      return 0;
    }
  printf("%d\n", out);
  for (int i = 1; i <= out; i++) printf("%d ", ans[i]);
  return 0;
}
