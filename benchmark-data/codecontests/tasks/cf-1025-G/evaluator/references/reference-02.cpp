#include <bits/stdc++.h>
struct {
  inline operator int() {
    int x;
    return scanf("%d", &x), x;
  }
  inline operator long long() {
    long long x;
    return scanf("%lld", &x), x;
  }
  template <class T>
  inline void operator()(T &x) {
    x = *this;
  }
  template <class T, class... A>
  inline void operator()(T &x, A &...a) {
    x = *this;
    this->operator()(a...);
  }
} read;
const int maxn = 505, mod = 1000000007;
int a[maxn];
int tot[maxn];
long long f[maxn];
int main() {
  int n = read;
  for (int i = 1; i <= n; i++) {
    read(a[i]);
    if (a[i] != -1) ++tot[a[i]];
  }
  for (int i = 1; i <= n; i++) f[i] = (f[i - 1] * 2 + 1) % mod;
  long long begin = 0;
  for (int i = 1; i <= n; i++) begin += f[tot[i]];
  begin %= mod;
  long long end = f[n - 1];
  printf("%lld\n", (end - begin + mod) % mod);
}
