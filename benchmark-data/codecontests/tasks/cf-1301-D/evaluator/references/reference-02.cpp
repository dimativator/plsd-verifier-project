#include <bits/stdc++.h>
using namespace std;
int n, m, k;
vector<pair<string, int> > ans;
void calc(string s, int v) {
  if (k > (int)s.size() * v) {
    ans.push_back(make_pair(s, v));
    k -= (int)s.size() * v;
  } else {
    int l = 1, r = v, f = -1;
    while (r >= l) {
      int mid = (r + l) / 2;
      if (mid * (int)s.size() <= k) {
        f = mid;
        l = mid + 1;
      } else {
        r = mid - 1;
      }
    }
    if (f != -1) {
      ans.push_back(make_pair(s, f));
      k -= (int)s.size() * f;
    }
    string d;
    for (int i = 0; i < k; i++) {
      d += s[i];
    }
    if ((int)d.size()) ans.push_back(make_pair(d, 1));
    cout << (int)ans.size() << endl;
    for (auto to : ans) {
      cout << to.second << ' ' << to.first << endl;
    }
    exit(0);
  }
}
int main() {
  cin >> n >> m >> k;
  int cnt = (4 * n * m - 2 * n - 2 * m);
  if (k > cnt) {
    cout << "NO" << endl;
    return 0;
  }
  cout << "YES" << endl;
  if (m == 1) {
    calc("D", n - 1);
    calc("U", n - 1);
  }
  calc("R", m - 1);
  calc("L", m - 1);
  for (int i = 1; i < n; i++) {
    calc("D", 1);
    calc("RUD", m - 1);
    calc("L", m - 1);
  }
  calc("U", n - 1);
  return 0;
}
