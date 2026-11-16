#include <bits/stdc++.h>
using namespace std;
const long long N = 2e6 + 5, K = 11, M = N * 4;
const long long MOD = 998244353, oo = 1e9, OO = 1e18, mod = MOD;
const double pi = acos(-1), eps = 1e-17;
long long di[] = {0, 0, 1, -1};
long long dj[] = {1, -1, 0, 0};
long long n, arr[2002];
long long ntprime[N];
void seive() {
  for (long long i = 2; i * i <= 2e6; i += (i == 2 ? 1 : 2)) {
    if (ntprime[i]) continue;
    for (long long j = i * i; j <= 2e6; j += i) ntprime[j]++;
  }
}
int32_t main() {
  ios_base::sync_with_stdio(false);
  cin.tie(0);
  ;
  seive();
  long long n;
  cin >> n;
  vector<long long> v(n);
  map<long long, long long> mp;
  vector<long long> ans;
  for (auto &it : v) {
    cin >> it;
    mp[it]++;
  }
  if (mp[1] > 1) {
    for (long long i = 0; i < mp[1]; i++) ans.push_back(1);
    for (long long i = 0; i < n; i++) {
      if (v[i] != 1 && !ntprime[1 + v[i]]) {
        ans.push_back(v[i]);
        break;
      }
    }
  } else {
    for (long long i = 0; i < n; i++) {
      for (long long j = i + 1; j < n; j++) {
        if (!ntprime[v[i] + v[j]]) {
          ans.push_back(v[i]);
          ans.push_back(v[j]);
          goto A;
        }
      }
    }
  }
A:
  if (ans.empty()) ans.push_back(v[0]);
  cout << ans.size() << '\n';
  for (auto f : ans) cout << f << " ";
}
