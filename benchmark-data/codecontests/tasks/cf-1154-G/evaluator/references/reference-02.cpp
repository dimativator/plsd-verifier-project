#include <bits/stdc++.h>
using namespace std;
const int N = 10000001;
int num[N], n;
long long ans = LLONG_MAX;
int t1, t2;
int main() {
  ios::sync_with_stdio(false);
  cin >> n;
  int tmp;
  for (int i = 1; i <= n; i++) {
    cin >> tmp;
    if (num[tmp] && tmp < ans) {
      ans = tmp;
      t1 = num[tmp];
      t2 = i;
    }
    if (!num[tmp]) num[tmp] = i;
  }
  for (int i = 1; i < N && i < ans; i++) {
    long long s1 = 0, s2 = 0;
    for (int j = i; j < N; j += i) {
      if (!num[j])
        continue;
      else if (!s1)
        s1 = j, s2 = num[j];
      else {
        if (ans > s1 * j / i) {
          ans = s1 * j / i;
          t1 = s2;
          t2 = num[j];
        }
        break;
      }
    }
  }
  if (t1 > t2) swap(t1, t2);
  cout << t1 << ' ' << t2 << endl;
  return 0;
}
