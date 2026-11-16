#include <bits/stdc++.h>
using namespace std;
int n, cnt, sum, now, a[100000];
long long ans;
int main() {
  scanf("%d", &n);
  for (int i = 0; i < n; i++) {
    scanf("%d", a + i);
    sum += a[i];
  }
  if (sum % 3) return puts("0");
  for (int i = 0; i < n - 1; i++) {
    now += a[i];
    if (now == sum / 3 * 2) ans += cnt;
    if (now == sum / 3) cnt++;
  }
  printf("%I64d\n", ans);
}
