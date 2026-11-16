#include <bits/stdc++.h>
using namespace std;
const int N = 4e5 + 10;
vector<int> G[N];
int n, m, degi[N], dego[N], drif;
vector<vector<int> > mat;
void Tsort() {
  queue<int> q;
  for (int i = 0; i < drif + 1; i++) {
    dego[i] = G[i].size();
    for (int j = 0; j < G[i].size(); j++) degi[G[i][j]]++;
  }
  int total = m;
  for (int i = 0; i < drif + 1; i++)
    if (!degi[i]) q.push(i);
  int cnt = 0;
  vector<int> ans;
  while (!q.empty()) {
    cnt++;
    int u = q.front();
    for (int i = 0; i < G[u].size(); i++) {
      degi[G[u][i]]--;
      if (degi[G[u][i]] == 0) q.push(G[u][i]);
    }
    ans.push_back(u);
    q.pop();
  }
  if (cnt < drif + 1) {
    cout << -1 << endl;
    return;
  }
  for (int i = 0; i < ans.size(); i++)
    if (ans[i] < m) cout << ans[i] + 1 << ' ';
  cout << endl;
}
int main() {
  ios::sync_with_stdio(false);
  cin >> n >> m;
  mat = vector<vector<int> >(n, vector<int>(m));
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < m; j++) {
      cin >> mat[i][j];
    }
  }
  drif = m;
  for (int i = 0; i < n; i++) {
    vector<pair<int, int> > nu;
    for (int j = 0; j < m; j++) {
      nu.push_back(make_pair(mat[i][j], j));
    }
    drif++;
    sort(nu.begin(), nu.end());
    for (int j = 0; j < m; j++) {
      if (nu[j].first == -1) {
        continue;
      }
      int pt = j;
      while (nu[j].first == nu[pt].first && pt < m) pt++;
      for (int k = j; k < pt; k++) {
        G[drif].push_back(nu[k].second);
      }
      drif++;
      for (int k = j; k < pt; k++) {
        G[nu[k].second].push_back(drif);
      }
      j = pt - 1;
    }
  }
  Tsort();
  return 0;
}
