#include <bits/stdc++.h>
using namespace std;
int n, m, u, v, k, vis[505];
char ans[505];
char mp[] = {'a', 'c', 'b'};
set<int> nodes[3];
vector<int> edges[505];
int main() {
  cin >> n >> m;
  while (m--) {
    scanf("%d %d", &u, &v);
    edges[u].push_back(v);
    edges[v].push_back(u);
  }
  bool same = true;
  for (u = 1; u <= n; ++u) {
    if (edges[u].size() != n - 1) {
      same = false;
      break;
    }
  }
  if (same) return printf("Yes\n%s", string(n, 'a').c_str()), 0;
  for (u = 1; u <= n && k < 2; ++u) {
    if (edges[u].size() == n - 1 || vis[u] > 0) {
      continue;
    }
    for (int v : edges[u]) {
      vis[v]++;
      nodes[k].insert(v);
    }
    nodes[k++].insert(u);
  }
  for (u = 1; u <= n; ++u) {
    if (vis[u] == 2) {
      nodes[0].erase(u);
      nodes[1].erase(u);
      nodes[2].insert(u);
    }
  }
  if (nodes[0].size() + nodes[1].size() + nodes[2].size() != n)
    return cout << "No", 0;
  for (k = 0; k < 2; ++k)
    for (int u : nodes[k])
      if (edges[u].size() != nodes[k].size() + nodes[2].size() - 1)
        return cout << "No", 0;
  for (int u : nodes[2])
    if (edges[u].size() !=
        nodes[0].size() + nodes[1].size() + nodes[2].size() - 1)
      return cout << "No", 0;
  for (k = 0; k < 3; ++k)
    for (int u : nodes[k]) ans[u] = mp[k];
  printf("Yes\n%s", ans + 1);
  return 0;
}
