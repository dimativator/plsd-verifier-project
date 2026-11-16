#include <bits/stdc++.h>
using namespace std;
const int N = 3e5 + 10;
const int oo = 1e9;
const int PI = acos(-1);
long long n, s1, best, s3;
int a[N];
vector<int> ans, ans2;
int main() {
  cin >> n;
  if (n == 1) return cout << 0, 0;
  for (int i = 0; i < n; i++) {
    scanf("%d", a + i);
  }
  long long c = 0;
  int i = n - 1, j = 0;
  while (true) {
    for (; i > -1; i--) {
      c++;
      s3 += a[i];
      if (s3 >= s1) {
        i--;
        break;
      }
    }
    if (s1 == s3) best = s1;
    if (c > n - 1 && s1 == s3)
      break;
    else if (c > n - 1 && s1 != s3) {
      s3 -= a[i + 1];
      c--;
    }
    for (; j < n; j++) {
      c++;
      s1 += a[j];
      if (s1 >= s3) {
        j++;
        break;
      }
    }
    if (s1 == s3) best = s1;
    if (c > n - 1) break;
  }
  cout << best;
  return 0;
}
