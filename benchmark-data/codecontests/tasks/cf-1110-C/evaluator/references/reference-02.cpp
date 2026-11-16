#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1e18;
const long long N = 2e5 + 5;
long long a[30];
long long gcd(long long a, long long b) {
  if (!b) return a;
  return gcd(b, a % b);
}
int main() {
  long long i, j, k;
  long long n, m, t;
  long long s = 1, l = 1;
  for (i = 1; i <= 26; i++) {
    s *= 2;
    a[l++] = s;
  }
  scanf("%I64d", &t);
  while (t--) {
    cin >> n;
    for (i = 1; i <= 26; i++) {
      if (n <= a[i]) {
        if (n == a[i]) {
          cout << a[i] * 2 - 1 << endl;
          break;
        }
        if (n == a[i] - 1) {
          long long f = 0;
          for (j = 2; j * j <= n; j++) {
            if (n % j == 0) {
              cout << n / j << endl;
              f = 1;
              break;
            }
          }
          if (!f) {
            cout << 1 << endl;
            break;
          } else
            break;
        }
        cout << a[i - 1] * 2 - 1 << endl;
        break;
      }
    }
  }
  return 0;
}
