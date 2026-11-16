#include <bits/stdc++.h>
using namespace std;
class TaskC {
 public:
  vector<pair<long long, long long> > v;
  vector<long long> ans;
  long long n, m;
  void rec(long long i, long long mx) {
    long long tmx = mx;
    long long ed = 0;
    long long j = v[i].first;
    while (j <= v[i].second && ans[j]) {
      j++;
      ed = max(ed, ans[j]);
    }
    j++;
    for (j; tmx != ed && j <= v[i].second; j++) {
      ans[j] = tmx--;
    }
    if (i != n - 1) rec(i + 1, mx);
  }
  void solve(std::istream& cin, std::ostream& cout) {
    cin >> n >> m;
    v.resize(m);
    ans.resize(n, false);
    long long mex = 1e18;
    for (long long i = 0; i < m; i++) {
      cin >> v[i].first >> v[i].second;
      v[i].first--, v[i].second--;
      mex = min(mex, v[i].second - v[i].first);
    }
    sort(v.begin(), v.end());
    cout << mex + 1 << endl;
    long long tmex = mex;
    for (long long i = 0; i < n; i++) {
      cout << tmex << ' ';
      tmex--;
      if (tmex < 0) tmex = mex;
    }
  }
};
int main() {
  TaskC solver;
  std::istream& in(std::cin);
  std::ostream& out(std::cout);
  solver.solve(in, out);
  return 0;
}
