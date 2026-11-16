#include <bits/stdc++.h>
using namespace std;
const int N = 2e5 + 5;
const int M = 4e5 + 10;
vector<int> vec[N], ans;
struct Edge {
  int to, next;
} edge[M];
int head[M], tot;
void init() {
  tot = 0;
  memset(head, -1, sizeof(head));
}
void addedge(int u, int v) {
  edge[tot].to = v;
  edge[tot].next = head[u];
  head[u] = tot++;
}
bool vis[N];
int S[N], top;
bool dfs(int u) {
  if (vis[u ^ 1]) return false;
  if (vis[u]) return true;
  vis[u] = true;
  S[top++] = u;
  for (int i = head[u]; i != -1; i = edge[i].next)
    if (!dfs(edge[i].to)) return false;
  return true;
}
bool Twosat(int n) {
  memset(vis, false, sizeof(vis));
  for (int i = 0; i < n; i += 2) {
    if (vis[i] || vis[i ^ 1]) continue;
    top = 0;
    if (!dfs(i)) {
      while (top) vis[S[--top]] = false;
      if (!dfs(i ^ 1)) return false;
    }
  }
  return true;
}
int main() {
  int n, m;
  int u, v;
  scanf("%d%d", &n, &m);
  init();
  for (int i = 1, s, x; i <= n; i++) {
    scanf("%d", &s);
    while (s--) {
      scanf("%d", &x);
      vec[i].push_back(x);
    }
    if (i == 1) continue;
    int len = min(vec[i].size(), vec[i - 1].size());
    int pos = -1;
    for (int j = 0; j < len; j++) {
      if (vec[i][j] != vec[i - 1][j]) {
        pos = j;
        break;
      }
    }
    if (pos == -1) {
      if (vec[i - 1].size() > vec[i].size()) {
        return puts("No") * 0;
      }
    } else {
      int a = vec[i - 1][pos], b = vec[i][pos];
      if (a > b) {
        addedge(2 * a - 1, 2 * a - 2);
        addedge(2 * b - 2, 2 * b - 1);
      } else {
        addedge(2 * a - 1, 2 * b - 1);
        addedge(2 * b - 2, 2 * a - 2);
      }
    }
  }
  if (Twosat(2 * m)) {
    puts("Yes");
    for (int i = 0; i < 2 * m; i += 2)
      if (vis[i]) ans.push_back((i) / 2 + 1);
    printf("%d\n", ans.size());
    for (int x : ans) printf("%d ", x);
  } else
    printf("No\n");
  return 0;
}
