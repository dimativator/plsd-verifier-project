#include <bits/stdc++.h>
using namespace std;
const long double EPS = 1e-9, PI = acos(-1.);
const int INF = 0x3f3f3f3f, MOD = 1e9 + 7;
const int N = 1e3 + 5, M = 1e6 + 5;
int n, a[N];
vector<int> v;
int main() {
  scanf("%d", &n);
  int ok = 1;
  for (int i = 0; i < n; i++) {
    scanf("%d", &a[i]);
    ok = ok && (a[i] % a[0] == 0);
  }
  if (ok) {
    printf("%d\n", 2 * n + 1);
    for (int i = 0; i < n; i++) printf("%d %d ", a[0], a[i]);
    printf("%d\n", a[0]);
  } else
    printf("-1\n");
  return 0;
}
