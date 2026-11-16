#include <bits/stdc++.h>
using namespace std;
void solve() {
  long long n;
  cin >> n;
  vector<long long> a(n);
  for (long long i = 0; i < n; i++) {
    cin >> a[i];
  }
  sort(a.begin(), a.end());
  vector<long long> neigh;
  long long j = n / 2;
  neigh.push_back(a[j++]);
  long long i = 0;
  long long ans = 0;
  for (; j < n; i++) {
    if (i != j && a[i] != a[j - 1])
      neigh.push_back(a[i]), ans++;
    else
      i--;
    neigh.push_back(a[j++]);
  }
  for (j = i; j < n / 2; j++) {
    neigh.push_back(a[j]);
  }
  cout << ans << endl;
  for (long long i = 0; i < neigh.size(); i++) {
    cout << neigh[i] << " ";
  }
}
int32_t main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);
  cout.tie(NULL);
  ;
  long long t = 1;
  while (t--) {
    solve();
    cout << endl;
  }
  return 0;
}
