#include <bits/stdc++.h>
using namespace std;
int dx[] = {1, 0, -1, 0, -1, -1, 1, 1};
int dy[] = {0, 1, 0, -1, -1, 1, -1, 1};
void fast() {
  std::ios_base::sync_with_stdio(0);
  cin.tie(NULL);
  cout.tie(NULL);
}
const int mxN = 3e5 + 5, oo = 0x3f3f3f3f, mod = 1e9 + 7;
void solve() {
  int n, m;
  cin >> n >> m;
  if (n == m && n == 1) {
    cout << 0 << "\n";
    return;
  }
  if (n == 1) {
    for (long long i = 1; i < m + 1; i++) cout << i + 1 << ' ';
  } else if (m == 1) {
    for (long long i = 1; i < n + 1; i++) cout << i + 1 << "\n";
  } else {
    for (long long i = 1; i < n + 1; i++) {
      for (long long j = 1; j < m + 1; j++) cout << i * (j + n) << ' ';
      cout << "\n";
      ;
    }
  }
}
int main() {
  fast();
  solve();
}
