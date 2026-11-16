#include <bits/stdc++.h>
using namespace std;
int main() {
  long long n, m, val;
  while (scanf("%I64d %I64d", &n, &m) == 2) {
    int cnt = 0, f;
    while (1) {
      if (n >= 2 and m >= 2) {
        n -= 2;
        m -= 2;
      } else if (n >= 1 and m >= 12) {
        n = n - 1;
        m = m - 12;
      } else if (m >= 22) {
        m -= 22;
      } else {
        f = 1;
        break;
      }
      if (m >= 22) {
        m -= 22;
      } else if (m >= 12 and n >= 1) {
        m = m - 12;
        n = n - 1;
      } else if (m >= 2 and n >= 2) {
        m -= 2;
        n -= 2;
      } else {
        f = 0;
        break;
      }
    }
    if (f == 0)
      cout << "Ciel" << endl;
    else
      cout << "Hanako" << endl;
  }
}
