#include <bits/stdc++.h>
using namespace std;
vector<int> clauses[200005];
bool cok[200005];
int val[200005], used[200005];
vector<pair<int, int> > E[200005];
int findRoot(int x, int p) {
  used[x] = 1;
  if (cok[x]) return x;
  for (auto &y : E[x]) {
    int a = y.first, b = y.second;
    if (abs(p) == abs(b)) continue;
    if (used[a]) return a;
    int u = findRoot(a, b);
    if (u != -1) return u;
  }
  return -1;
}
void assign(int x, int p) {
  if (used[x] == 2) return;
  used[x] = 2;
  for (auto &y : E[x]) {
    int a = y.first, b = y.second;
    if (abs(p) == abs(b)) continue;
    if (val[abs(b)] == -1) val[abs(b)] = b > 0;
    assign(a, b);
  }
}
int main() {
  int N, M;
  scanf("%d%d", &N, &M);
  for (int i = 1; i <= N; ++i) {
    int K;
    scanf("%d", &K);
    for (int j = 0; j < K; ++j) {
      int a;
      scanf("%d", &a);
      clauses[abs(a)].push_back(a < 0 ? -i : i);
    }
  }
  memset(val, -1, sizeof(val));
  for (int i = 1; i <= M; ++i) {
    vector<int> &vec = clauses[i];
    if (vec.empty()) {
      val[i] = 1;
    } else if (vec.size() == 1 || (vec[0] < 0) == (vec[1] < 0)) {
      val[i] = vec[0] > 0;
      cok[abs(vec[0])] = true;
      if (vec.size() > 1) cok[abs(vec[1])] = true;
    } else {
      int a = vec[0], b = vec[1];
      if (a > b) swap(a, b);
      E[-a].push_back(make_pair(b, i));
      E[b].push_back(make_pair(-a, -i));
    }
  }
  for (int i = 1; i <= N; ++i) {
    if (used[i]) continue;
    int u = findRoot(i, 0);
    if (u == -1) {
      printf("NO\n");
      return 0;
    }
    assign(u, 0);
  }
  printf("YES\n");
  for (int i = 1; i <= M; ++i) printf("%d", val[i]);
  printf("\n");
}
