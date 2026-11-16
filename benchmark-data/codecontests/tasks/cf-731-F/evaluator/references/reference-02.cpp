#include <bits/stdc++.h>
using namespace std;
long long a[400200], cnt[400200];
int vis[200100];
int main() {
  long long n, sum = 0;
  scanf("%I64d", &n);
  for (int i = 0; i < n; i++) {
    scanf("%I64d", &a[i]);
    sum += a[i];
    ++cnt[a[i]];
  }
  sort(a, a + n);
  for (int i = 1; i <= 400100; i++) cnt[i] += cnt[i - 1];
  long long ans = 0;
  for (int i = 0; i < n; i++) {
    if (vis[a[i]]) continue;
    if (a[i] == 1) {
      ans = max(ans, sum);
      vis[1] = 1;
      continue;
    }
    vis[a[i]] = 1;
    long long tmp = 0;
    long long k = 1;
    while (k * a[i] <= a[n - 1]) {
      tmp += (cnt[a[i] * (k + 1) - 1] - cnt[a[i] * (k)-1]) * a[i] * k;
      k++;
    }
    if (tmp > ans) ans = tmp;
  }
  printf("%I64d\n", ans);
  return 0;
}
