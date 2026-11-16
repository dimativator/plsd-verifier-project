#include <bits/stdc++.h>
#pragma comment(linker, "/STACK:256000000")
using namespace std;
const long double PI = 3.14159265358979323846;
const long double eps = 1e-5;
const int INF = numeric_limits<int>::max();
const long long LINF = numeric_limits<long long>::max();
const long long mod = 1000 * 1000 * 1000 + 7;
vector<vector<pair<long long, long long> > > g;
vector<int> leave;
void dfs(int pos, int pr = -1) {
  int to = -1;
  for (int i = 0; i < g[pos].size(); ++i) {
    if (g[pos][i].first == pr) continue;
    to = g[pos][i].first;
    break;
  }
  if (to == -1) {
    leave[pos] = pos;
    return;
  }
  int tot = to;
  for (int i = 0; i < g[pos].size(); ++i) {
    if (g[pos][i].first == pr) continue;
    to = g[pos][i].first;
    dfs(to, pos);
  }
  leave[pos] = leave[tot];
}
vector<pair<int, int> > res1;
vector<long long> res2;
void dfs2(int pos, long long add, int leaf, int pr = -1) {
  vector<int> l;
  vector<long long> c;
  for (int i = 0; i < g[pos].size(); ++i) {
    int to = g[pos][i].first;
    if (to == pr) continue;
    l.push_back(to);
    c.push_back(g[pos][i].second);
  }
  if (c.empty()) return;
  c[0] -= add;
  if (c.size() == 2) {
    long long x = (c[0] - c[1]) / 2;
    res1.push_back(pair<int, int>(leave[l[0]], leaf));
    res2.push_back(x);
    res1.push_back(pair<int, int>(leave[l[1]], leaf));
    res2.push_back(-x);
    long long y = c[0] - x;
    res1.push_back(pair<int, int>(leave[l[0]], leave[l[1]]));
    res2.push_back(y);
  } else {
    long long c0 = c[0];
    for (int i = 3; i < l.size(); ++i) {
      res1.push_back(pair<int, int>(leave[l[0]], leave[l[i]]));
      res2.push_back(c[i]);
      c0 -= c[i];
    }
    long long d0 = (c0 + c[1] - c[2]) / 2;
    res1.push_back(pair<int, int>(leave[l[0]], leave[l[1]]));
    res2.push_back(d0);
    long long d1 = (c0 + c[2] - c[1]) / 2;
    res1.push_back(pair<int, int>(leave[l[0]], leave[l[2]]));
    res2.push_back(d1);
    long long d2 = (c[1] + c[2] - c0) / 2;
    res1.push_back(pair<int, int>(leave[l[1]], leave[l[2]]));
    res2.push_back(d2);
  }
  dfs2(l[0], c[0] + add, leave[l[1]], pos);
  for (int i = 1; i < l.size(); ++i) {
    dfs2(l[i], c[i], leave[l[0]], pos);
  }
}
void solve() {
  int n;
  cin >> n;
  vector<int> d(n, 0);
  g.resize(n);
  long long a, b, c;
  for (int i = 0; i < n - 1; ++i) {
    cin >> a >> b >> c;
    --a, --b;
    ++d[a];
    ++d[b];
    g[a].push_back(pair<int, int>(b, c));
    g[b].push_back(pair<int, int>(a, c));
  }
  for (int i = 0; i < n; ++i) {
    if (d[i] == 2) {
      cout << "NO\n";
      return;
    }
  }
  if (n == 2) {
    cout << "YES\n";
    cout << 1 << endl;
    cout << 1 << " " << 2 << " " << g[0][0].second << endl;
    return;
  }
  int st = 0;
  while (d[st] == 1) ++st;
  leave.resize(n);
  dfs(st, -1);
  dfs2(st, 0, -1, -1);
  cout << "YES\n";
  cout << res1.size() << endl;
  for (int i = 0; i < res1.size(); ++i) {
    cout << res1[i].first + 1 << " " << res1[i].second + 1 << " " << res2[i]
         << "\n";
  }
}
int main() {
  ios_base::sync_with_stdio(0);
  cin.tie(nullptr);
  cout.tie(nullptr);
  solve();
  return 0;
}
