#include <bits/stdc++.h>
using namespace std;
struct pt {
  int x, y, id;
};
vector<pt> p;
vector<vector<int> > g;
vector<int> size, ans;
int n;
int dfs(int v, int parent = -1) {
  for (int i = 0; i < g[v].size(); i++) {
    int to = g[v][i];
    if (to == parent) continue;
    size[v] += dfs(to, v);
  }
  return size[v];
}
int gx, gy;
bool cmp(pt a, pt b) {
  return 1LL * (a.x - gx) * (b.y - gy) - 1LL * (b.x - gx) * (a.y - gy) > 0;
}
bool cmp2(pt a, pt b) { return a.y > b.y || a.y == b.y && a.x < b.x; }
void rec(int v, vector<pt> p, int parent = -1) {
  gx = p.front().x, gy = p.front().y;
  ans[p.front().id] = v;
  p.erase(p.begin());
  sort(p.begin(), p.end(), cmp);
  vector<pt> buf;
  int cur = 0;
  for (int i = 0; i < g[v].size(); i++) {
    int to = g[v][i];
    if (to != parent) {
      buf.clear();
      for (int x = cur; cur < x + size[to]; cur++) {
        buf.push_back(p[cur]);
      }
      rec(to, buf, v);
    }
  }
}
int main() {
  cin >> n;
  g.resize(n);
  p.resize(n);
  ans.resize(n);
  size.assign(n, 1);
  for (int i = 0; i < n - 1; i++) {
    int a, b;
    cin >> a >> b;
    g[--a].push_back(--b);
    g[b].push_back(a);
  }
  for (int i = 0; i < n; i++) {
    cin >> p[i].x >> p[i].y;
    p[i].id = i;
  }
  dfs(0);
  sort(p.begin(), p.end(), cmp2);
  rec(0, p);
  for (int i = 0; i < n; i++) cout << (ans[i] + 1) << " ";
  return 0;
}
