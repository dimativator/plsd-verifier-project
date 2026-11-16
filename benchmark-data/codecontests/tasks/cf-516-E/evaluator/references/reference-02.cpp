#include <bits/stdc++.h>
using namespace std;
int a[101], b[101];
int main() {
  int n, m, i;
  cin >> n >> m;
  memset(a, 0, sizeof(a));
  memset(b, 0, sizeof(b));
  int x, y;
  cin >> x;
  int e;
  for (i = 1; i <= x; i++) {
    cin >> e;
    a[e] = 1;
  }
  cin >> y;
  for (i = 1; i <= y; i++) {
    cin >> e;
    b[e] = 1;
  }
  for (i = 0; i < 100000; i++) {
    if (a[i % n] + b[i % m] > 0) {
      a[i % n] = 1;
      b[i % m] = 1;
    }
  }
  for (i = 0; i < n; i++) {
    if (a[i] == 0) break;
  }
  if (i != n) {
    cout << "No" << endl;
    return 0;
  }
  for (i = 0; i < m; i++) {
    if (b[i] == 0) break;
  }
  if (i != m) {
    cout << "No" << endl;
    return 0;
  }
  cout << "Yes" << endl;
}
