#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, m;
  scanf("%d", &n);
  int a[n + 10];
  for (int i = 1; i <= n; i++) scanf("%d", &a[i]);
  scanf("%d", &m);
  int b[m + 10];
  for (int i = 1; i <= m; i++) scanf("%d", &b[i]);
  int local, ans = 0, indx;
  int Max[m + 10];
  memset(Max, 0, sizeof Max);
  vector<int> path[505];
  for (int i = 1; i <= n; i++) {
    local = 0;
    for (int j = 1; j <= m; j++) {
      if (a[i] == b[j]) {
        Max[j] = max(Max[j], local + 1);
        if (local + 1 > ans) {
          indx = j;
          ans = local + 1;
        }
        path[Max[j]].push_back(j);
      } else if (a[i] > b[j])
        local = max(Max[j], local);
    }
  }
  cout << ans << endl;
  int val = 1000000001;
  vector<int> Ans;
  int in = 50001;
  while (ans) {
    for (int i = 0; i < path[ans].size(); i++) {
      if (val > b[path[ans][i]] && in > path[ans][i]) {
        Ans.push_back(b[path[ans][i]]);
        val = b[path[ans][i]];
        in = path[ans][i];
        ans--;
        break;
      }
    }
  }
  reverse(Ans.begin(), Ans.end());
  for (int i = 0; i < Ans.size(); i++) cout << Ans[i] << " ";
  cout << endl;
  return 0;
}
