#include <bits/stdc++.h>
using namespace std;
const int kMax = 50;
bool mp[510][510];
bool vis[510];
int link[510];
int in[510], out[510];
int n, m;
bool dfs(int cur, int u) {
  for (int i = 1; i <= n; i++) {
    if (i == cur) continue;
    if (!vis[i] && mp[u][i]) {
      vis[i] = 1;
      if (!link[i] || dfs(cur, link[i])) {
        link[i] = u;
        return true;
      }
    }
  }
  return false;
}
int max_match(int cur) {
  int s = (in[cur] + out[cur] - (int)mp[cur][cur]);
  int ans = 2 * n - 1 - s;
  int tmp = 0;
  memset(link, 0, sizeof(link));
  for (int i = 1; i <= n; i++) {
    if (i == cur) continue;
    memset(vis, 0, sizeof vis);
    if (dfs(cur, i)) tmp++;
  }
  ans = ans + m - s - tmp;
  ans = ans + n - 1 - tmp;
  return ans;
}
signed main() {
  scanf("%d%d", &n, &m);
  for (int i = 1; i <= m; ++i) {
    int u, v;
    scanf("%d%d", &u, &v);
    mp[u][v] = 1;
    out[u]++;
    in[v]++;
  }
  int res = INT_MAX;
  for (int i = 1; i <= n; i++) res = min(res, max_match(i));
  cout << res << '\n';
  return 0;
}
