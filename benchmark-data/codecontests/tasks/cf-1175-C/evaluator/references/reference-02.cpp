#include <bits/stdc++.h>
using namespace std;
long long n, m, x, k, t;
int const MAX_N = 2 * 100000;
int main() {
  cin >> t;
  while (t--) {
    cin >> n >> k;
    vector<int> vec(n);
    for (int i = 0; i < n; i++) {
      cin >> vec[i];
    }
    int mini = 2000000000;
    int res = 0;
    for (int i = 0; i < n - k; i++) {
      int check = vec[k + i] - vec[i];
      if (check % 2 != 0) {
        if (check / 2 + 1 < mini) {
          mini = (check) / 2 + 1;
          res = vec[i] + mini;
        }
      } else {
        if ((vec[k + i] - vec[i]) / 2 < mini) {
          mini = (vec[k + i] - vec[i]) / 2;
          res = vec[i] + mini;
        }
      }
    }
    cout << res << endl;
  }
}
