#include <bits/stdc++.h>
using namespace std;
signed main() {
  ios_base::sync_with_stdio(false);
  cin.tie(0);
  long long n, m, k;
  cin >> n >> m >> k;
  vector<long long> a(n);
  for (auto &t : a) {
    cin >> t;
  }
  vector<long long> ind;
  for (long long i = 0; i < n; i++) {
    ind.push_back(i);
  }
  sort(ind.rbegin(), ind.rend(),
       [&](long long i, long long j) { return a[i] < a[j]; });
  long long ans = 0;
  vector<long long> cut(m * k);
  for (long long i = 0; i < m * k; i++) {
    ans += a[ind[i]];
    cut[i] = ind[i];
  }
  sort(cut.begin(), cut.end());
  cout << ans << '\n';
  long long cnt = 0;
  long long uu = 0;
  for (long long i = 0; i < n; i++) {
    auto it = lower_bound(cut.begin(), cut.end(), i);
    bool fl = false;
    if (it != cut.end() && *(it) == i) {
      fl = true;
    }
    if (fl) {
      cnt++;
    }
    if (cnt == m && uu < k - 1) {
      uu++;
      cnt = 0;
      cout << i + 1 << ' ';
    }
  }
}
