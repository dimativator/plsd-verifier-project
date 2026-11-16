#include <bits/stdc++.h>
using ll = long long;
using namespace std;
const ll N = 1e5 + 1;
ll connec[N], n, dd[N];
vector<ll> a[N], f, s;
ll dfs(ll u) {
  for (auto v : a[u])
    if (!dd[v]) {
      dd[v] = 1;
      return dfs(v);
    }
  return u;
}
ll cnt1 = 0, cnt2 = 0;
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> n;
  for (ll i = 1; i <= n; i++) {
    ll x;
    cin >> x;
    a[i].push_back(x);
    connec[x] = 1;
  }
  f.push_back(0);
  for (ll i = 1; i <= n; i++)
    if (!connec[i]) {
      s.push_back(i);
      dd[i] = 1;
      f.push_back(dfs(i));
      cnt1++;
    }
  for (ll i = 1; i <= n; i++)
    if (!dd[i]) {
      dd[i] = 1;
      s.push_back(i);
      f.push_back(dfs(i));
      cnt2++;
    }
  if (cnt2 == 1 && cnt1 == 0) return cout << 0, 0;
  cout << cnt1 + cnt2 << '\n';
  for (ll i = 1; i <= s.size() - 1; i++) cout << f[i] << " " << s[i] << '\n';
  cout << f[f.size() - 1] << " " << s[0];
}
