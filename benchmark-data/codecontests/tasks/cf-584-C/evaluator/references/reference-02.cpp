#include <bits/stdc++.h>
using namespace std;
constexpr int MAXN = 100000;
char s1[MAXN + 2], s2[MAXN + 2], ans[MAXN + 2];
char neither(char a, char b) {
  if (a > b) swap(a, b);
  char x = 'a';
  if (a == x) x++;
  if (b == x) x++;
  return x;
}
int main() {
  int n, t;
  cin >> n >> t >> s1 >> s2;
  t = n - t;
  for (int i = 0; i < n; i++) {
    if (s1[i] == s2[i]) {
      if (t) {
        ans[i] = s1[i];
        --t;
      } else {
        ans[i] = s1[i] == 'a' ? 'b' : 'a';
      }
    }
  }
  bool lst = false;
  for (int i = 0; i < n; i++) {
    if (s1[i] != s2[i]) {
      if (t) {
        if (!lst) {
          ans[i] = s1[i];
          lst ^= 1;
        } else {
          ans[i] = s2[i];
          lst ^= 1;
          --t;
        }
      } else {
        ans[i] = neither(s1[i], s2[i]);
      }
    }
  }
  if (t == 0)
    cout << ans << '\n';
  else
    cout << -1 << '\n';
}
