#include <bits/stdc++.h>
using namespace std;
template <typename T>
void out(T x) {
  cout << x << endl;
  exit(0);
}
const int maxn = 1e6 + 11;
string solve() {
  int n;
  cin >> n;
  vector<pair<int, int>> v(n);
  vector<int> cnt = {0, 0};
  vector<int> checksorted(n);
  for (int i = 0; i < n; i++) {
    cin >> v[i].first;
    checksorted[i] = v[i].first;
  }
  for (int i = 0; i < n; i++) {
    cin >> v[i].second;
    cnt[v[i].second]++;
  }
  sort(checksorted.begin(), checksorted.end());
  bool sorted = true;
  for (int i = 0; i < n; i++) {
    if (checksorted[i] != v[i].first) {
      sorted = false;
      break;
    }
  }
  if (sorted) return "Yes";
  if (cnt[0] == 0) return "No";
  if (cnt[1] == 0) return "No";
  return "Yes";
}
int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(0);
  cout.tie(0);
  int T;
  cin >> T;
  while (T--) {
    cout << solve() << "\n";
  }
  return 0;
}
