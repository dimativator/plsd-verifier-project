#include <bits/stdc++.h>
using namespace std;
int mu[66];
void init() {
  mu[1] = 1;
  for (int i = 1; i <= 59; i++)
    for (int j = i * 2; j <= 59; j += i) mu[j] -= mu[i];
}
void solve() {
  long long n, ans;
  scanf("%lld", &n);
  ans = n - 1;
  for (int i = 2; i <= 59; i++) {
    if (!mu[i]) continue;
    long long limit = (long long)pow(n, 1.0 / i);
    for (;;) {
      limit++;
      long long tmp = n;
      for (int j = 1; j <= i; j++) tmp /= limit;
      if (!tmp) {
        limit--;
        break;
      }
    }
    ans += (limit - 1) * mu[i];
  }
  printf("%lld\n", ans);
}
int main() {
  init();
  int T;
  scanf("%d", &T);
  while (T--) solve();
}
