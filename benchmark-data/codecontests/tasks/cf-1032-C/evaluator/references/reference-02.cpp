#include <bits/stdc++.h>
using namespace std;
const long long mod = 1000000007;
const long long INF = 10000000000;
long long power(long long a, long long b) {
  long long res = 1;
  a %= mod;
  assert(b >= 0);
  for (; b; b >>= 1) {
    if (b & 1) res = res * a % mod % mod;
    a = a * a % mod;
  }
  return res;
}
int main() {
  ios::sync_with_stdio(0);
  cin.tie(0);
  cout.tie(0);
  ;
  long long i, j, k, t, n, m;
  cin >> n;
  long long a[n];
  for (i = 0; i < n; i++) {
    cin >> a[i];
  }
  long long b[n];
  if (n == 1) {
    cout << 1 << "\n";
  } else {
    if (a[0] < a[1]) {
      b[0] = 1;
    } else if (a[0] > a[1]) {
      b[0] = 5;
    } else {
      b[0] = 3;
    }
    for (i = 1; i < n; i++) {
      if (a[i - 1] < a[i]) {
        if (i < n - 1 && a[i + 1] > a[i]) {
          b[i] = b[i - 1] + 1;
        } else if (i < n - 1 && a[i + 1] < a[i]) {
          b[i] = 5;
          if (b[i - 1] == 5) {
            cout << -1 << "\n";
            return 0;
          }
        } else {
          b[i] = b[i - 1] + 1;
        }
      } else if (a[i] < a[i - 1]) {
        if (i < n - 1 && a[i + 1] < a[i]) {
          b[i] = b[i - 1] - 1;
        } else if (i < n - 1 && a[i + 1] > a[i]) {
          b[i] = 1;
          if (b[i - 1] == 1) {
            cout << -1 << "\n";
            return 0;
          }
        } else {
          b[i] = b[i - 1] - 1;
        }
      } else {
        if (i < n - 1 && a[i + 1] > a[i]) {
          b[i] = 1;
          if (b[i - 1] == 1) {
            b[i] = 2;
          }
        } else if (i < n - 1 && a[i + 1] < a[i]) {
          b[i] = 5;
          if (b[i - 1] == 5) {
            b[i] = 4;
          }
        } else {
          if (b[i - 1] != 3) {
            b[i] = 3;
          } else if (b[i - 1] != 4) {
            b[i] = 4;
          }
        }
      }
    }
    for (i = 0; i < n; i++) {
      if (b[i] < 1 || b[i] > 5) {
        cout << -1 << "\n";
        return 0;
      }
    }
    for (i = 0; i < n; i++) {
      cout << b[i] << " ";
    }
  }
  return 0;
}
