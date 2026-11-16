#include <bits/stdc++.h>
using namespace std;
inline void timer(void) {
  int t = clock();
  cout << (float(t)) / CLOCKS_PER_SEC;
}
int main() {
  int n, a, b, x, y, x_ = 0;
  cin >> n >> x >> y;
  if (!(y % x))
    if (!(n % x))
      return !(cout << "YES" << endl << n / x << ' ' << 0);
    else
      return !(cout << "NO");
  else
    while (n % y && n > 0) n -= x, x_++;
  if (n >= 0) return !(cout << "YES" << endl << x_ << ' ' << n / y);
  return !(cout << "NO");
}
