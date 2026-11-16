#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, i, j, k, p, t, ij, r;
  int a[101], b[101][101] = {0};
  cin >> n >> k;
  for (i = 1; i <= n; i++) cin >> a[i];
  for (i = 1; i <= n; i++) {
    t = a[i] / k;
    r = a[i] % k;
    for (j = 1; j <= r; j++) b[i][j] = t + 1;
    for (j = r + 1; j <= a[i]; j++) b[i][j] = t;
  }
  for (i = 1; i < n; i++)
    for (j = i + 1; j <= n; j++)
      for (ij = 1; ij <= k; ij++)
        if (b[i][ij] - b[j][ij] > 1 || b[j][ij] - b[i][ij] > 1) {
          cout << "NO\n";
          return 0;
        }
  cout << "YES\n";
  for (i = 1; i <= n; i++) {
    for (j = 1; j <= k; j++) {
      for (ij = 1; ij <= b[i][j]; ij++) cout << j << " ";
    }
    cout << endl;
  }
}
