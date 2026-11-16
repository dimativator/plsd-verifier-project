#include <bits/stdc++.h>
using namespace std;
const int N = 1017;
int main() {
  ios_base::sync_with_stdio(0);
  cin.tie(0);
  int n, k;
  cin >> n >> k;
  if (k > 3) return cout << -1 << '\n', 0;
  if (k == 1) return cout << -1 << '\n', 0;
  if (k == 2 && n <= 4) return cout << -1 << '\n', 0;
  if (k == 3 && n <= 3) return cout << -1 << '\n', 0;
  if (k == 2) {
    cout << n - 1 << '\n';
    for (int i = 1; i < n; i++) cout << i << ' ' << i + 1 << '\n';
    return 0;
  } else if (k == 3) {
    cout << n - 1 << '\n';
    for (int i = 2; i < n; i++) cout << 1 << ' ' << i << '\n';
    cout << 2 << ' ' << n << '\n';
    return 0;
  }
}
