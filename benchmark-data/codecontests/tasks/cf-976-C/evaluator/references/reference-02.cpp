#include <bits/stdc++.h>
using namespace std;
const long long N = (long long)(1e5) + 10, mod = (long long)(1e9 + 7);
const long long INF = 1e17;
long long dp[N];
int main() {
  ios::sync_with_stdio(0);
  cin.tie(0);
  long long n;
  cin >> n;
  map<pair<long long, long long>, long long> cnt;
  vector<pair<long long, long long> > v(n);
  vector<pair<long long, long long> > v2(n);
  for (int i = 0; i < n; i++) {
    long long a, b;
    cin >> a >> b;
    v[i] = {a, b};
    v2[i] = {a, b};
    if (cnt[{a, b}] == 0) cnt[{a, b}] = i + 1;
  }
  sort(v.begin(), v.end());
  long long minn = v[0].second;
  long long ind = 1;
  long long firstminn = v[0].first;
  if (n == 1)
    cout << -1 << ' ' << -1 << '\n';
  else {
    bool possible = false;
    long long firstind = 0, secondind = 0;
    for (int i = 1; i < n; i++) {
      if (v[i].first != v[i - 1].first && v[i].second > v[i - 1].second) {
        firstminn = v[i].first;
        minn = v[i].second;
      } else {
        possible = true;
        if (v[i].first == v[i - 1].first && v[i].second == v[i - 1].second) {
          long long dd = cnt[{v[i - 1].first, v[i - 1].second}];
          bool printed = false;
          for (int j = 0; j < n; j++) {
            if (v2[j].first == v[i - 1].first &&
                v2[j].second == v[i - 1].second && j + 1 != dd) {
              cout << j + 1 << ' ' << dd;
              printed = true;
            }
            if (printed == true) break;
          }
          break;
        } else {
          if (v[i - 1].first == v[i].first)
            cout << cnt[{v[i - 1].first, v[i - 1].second}] << ' '
                 << cnt[{v[i].first, v[i].second}];
          else
            cout << cnt[{v[i].first, v[i].second}] << ' '
                 << cnt[{v[i - 1].first, v[i - 1].second}];
          break;
        }
      }
    }
    if (possible == false) cout << -1 << ' ' << -1 << '\n';
  }
}
