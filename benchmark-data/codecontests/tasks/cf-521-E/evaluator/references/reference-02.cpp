#include <bits/stdc++.h>
using namespace std;
const int N = 200010;
struct edge {
  int from, to, next;
} e[N * 20], e2[N * 10];
int head[N], ecnt, vis[N], fa[N][18], dep[N], ok[N * 10], ecnt2;
map<pair<int, int>, int> mp;
inline void adde(int from, int to) {
  e[++ecnt] = (edge){from, to, head[from]}, head[from] = ecnt;
  e[++ecnt] = (edge){to, from, head[to]}, head[to] = ecnt;
}
int fir, sec;
vector<int> G[N];
void dfs(int u, int f) {
  fa[u][0] = f, dep[u] = dep[f] + 1, vis[u] = 1;
  for (int i = 1; i <= 17; i++) fa[u][i] = fa[fa[u][i - 1]][i - 1];
  for (auto v : G[u])
    if (!vis[v]) {
      adde(v, u);
      int a = v, b = u;
      if (a > b) swap(a, b);
      ok[mp[pair<int, int>(a, b)]] = 1, dfs(v, u);
    }
}
inline int LCA(int a, int b) {
  if (dep[a] < dep[b]) swap(a, b);
  for (int i = 17; i >= 0; i--)
    if (dep[fa[a][i]] >= dep[b]) a = fa[a][i];
  if (a == b) return a;
  for (int i = 17; i >= 0; i--)
    if (fa[a][i] != fa[b][i]) a = fa[a][i], b = fa[b][i];
  return fa[a][0];
}
set<int> add[N], del[N], fuck[N];
bool flg;
inline void mark(int a, int b, int id) {
  int lca = LCA(a, b);
  add[a].insert(id), add[b].insert(id), del[lca].insert(id);
}
void dfs2(int u, int f) {
  for (int i = head[u]; i && !flg; i = e[i].next)
    if (e[i].to != f) dfs2(e[i].to, u);
  if (flg) return;
  for (auto v : add[u]) fuck[u].insert(v);
  for (int i = head[u]; i; i = e[i].next)
    if (e[i].to != f && fuck[e[i].to].size())
      fuck[u].insert(*fuck[e[i].to].begin());
  for (auto v : del[u]) fuck[u].erase(v);
  if (fuck[u].size() >= 2) {
    fir = *fuck[u].begin(), fuck[u].erase(fuck[u].begin()),
    sec = *fuck[u].begin();
    flg = true;
  }
}
int tmp[N], to, stk[N], top, hh, tmp2[N * 10];
void dfs3(int u) {
  if (u == to) {
    hh = 1, printf("%d ", top);
    for (int i = 1; i <= top; i++) printf("%d ", stk[i]);
    puts("");
    return;
  }
  tmp[u] = 1;
  for (auto v : G[u])
    if (!tmp[v]) {
      int a = u, b = v;
      if (a > b) swap(a, b);
      int t = mp[pair<int, int>(a, b)];
      if (tmp2[t]) continue;
      if (!ok[t] && t != fir && t != sec) continue;
      tmp2[t] = 1, stk[++top] = v, dfs3(v), top--;
      if (hh) return;
    }
}
inline void work(int a1, int a2, int b1, int b2) {
  static int p[5];
  p[1] = LCA(a1, b1), p[2] = LCA(a1, b2), p[3] = LCA(a2, b1),
  p[4] = LCA(a2, b2);
  sort(p + 1, p + 5, [](int a, int b) { return dep[a] > dep[b]; });
  int A = p[1], B = p[2];
  hh = 0, to = B, stk[top = 1] = A, dfs3(A), hh = 0, top = 1, dfs3(A), hh = 0,
  top = 1, dfs3(A);
}
int main() {
  int n, m;
  scanf("%d%d", &n, &m);
  for (int i = 1, a, b; i <= m; i++) {
    scanf("%d%d", &a, &b);
    if (a > b) swap(a, b);
    G[a].push_back(b), G[b].push_back(a), e2[++ecnt2] = (edge){a, b, 0},
                                          mp[pair<int, int>(a, b)] = ecnt2;
  }
  for (int i = 1; i <= n; i++)
    if (!vis[i]) dfs(i, 0);
  for (int i = 1; i <= ecnt2; i++)
    if (!ok[i]) mark(e2[i].from, e2[i].to, i);
  for (int i = 1; i <= n; i++)
    if (!fa[i][0]) {
      dfs2(i, 0);
      if (flg) {
        puts("YES"), work(e2[fir].from, e2[fir].to, e2[sec].from, e2[sec].to);
        return 0;
      }
    }
  puts("NO");
  return 0;
}
