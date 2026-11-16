#include <bits/stdc++.h>
using namespace std;
const long long MAXN = 500005;
vector<long long> g[MAXN];
long long ind;
pair<long long, long long> ans[MAXN];
void dfs(long long v, long long p) {
  for (long long i = (long long)g[v].size() - 1; i >= 0; i--) {
    if (g[v][i] != p) {
      ans[g[v][i]].second = ind--;
    }
  }
  ans[v].first = ind--;
  for (long long to : g[v]) {
    if (to != p) {
      dfs(to, v);
    }
  }
}
signed main() {
  cin.tie(0);
  cout.tie(0);
  ios_base ::sync_with_stdio(0);
  long long n;
  cin >> n;
  ind = n * 2;
  for (long long i = 0; i < n - 1; i++) {
    long long x, y;
    cin >> x >> y;
    x--;
    y--;
    g[x].push_back(y);
    g[y].push_back(x);
  }
  ans[0].second = ind--;
  dfs(0, -1);
  for (long long i = 0; i < n; i++) {
    cout << ans[i].first << ' ' << ans[i].second << '\n';
  }
  return 0;
}
