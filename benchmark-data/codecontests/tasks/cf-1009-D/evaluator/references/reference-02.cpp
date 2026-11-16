#include <bits/stdc++.h>
using namespace std;
const double eps = 1e-8;
const double inf = 1e20;
const double pi = acos(-1.0);
const int maxn = 1e6 + 7;
long long vis[2][maxn];
long long gcd(long long a, long long b) { return b == 0 ? a : gcd(b, a % b); }
int main() {
  long long n, m;
  while (cin >> n >> m) {
    if (m < n - 1) {
      puts("Impossible");
      continue;
    }
    long long k = 0;
    memset(vis, 0, sizeof(vis));
    for (long long i = 1; i < n; i++) {
      for (long long j = i + 1; j <= n; j++) {
        if (gcd(i, j) == 1) {
          vis[0][k] = i;
          vis[1][k] = j;
          k++;
          if (k > m) {
            break;
          }
        }
      }
    }
    if (k < m)
      puts("Impossible");
    else {
      puts("Possible");
      for (int i = 0; i < m; i++) {
        printf("%lld %lld\n", vis[0][i], vis[1][i]);
      }
    }
  }
  return 0;
}
