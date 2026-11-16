#include <bits/stdc++.h>
#pragma GCC optimize("Ofast")
#pragma GCC target("avx,avx2,fma")
using namespace std;
bool pal(string s, long long n) {
  for (long long i = 0; i < n / 2; i++) {
    if (s[i] != s[n - i - 1]) return false;
  }
  return true;
}
void solve() {
  string s;
  cin >> s;
  long long n = s.length();
  if (pal(s, n)) {
    cout << 0 << "\n";
    return;
  } else {
    cout << 3 << "\n";
    cout << "L " << 2 << "\n";
    cout << "R " << 2 << "\n";
    cout << "R " << 2 * n - 1 << "\n";
  }
}
int32_t main() {
  ios_base::sync_with_stdio(0);
  cin.tie(0);
  cout.tie(0);
  solve();
  return 0;
}
