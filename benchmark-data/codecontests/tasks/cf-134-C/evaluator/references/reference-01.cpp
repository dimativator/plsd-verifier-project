#include <bits/stdc++.h>
using namespace std;
const int maxn = 200001;
struct DIY {
  int x, y;
};
DIY a[maxn], h[maxn], ans[maxn], t;
int n, s, m, len = 0;
void down(int x) {
  int y;
  while ((x * 2 <= m) && (h[x * 2].x > h[x].x) ||
         (x * 2 + 1 <= m) && (h[x * 2 + 1].x > h[x].x)) {
    y = x * 2;
    if ((y + 1 <= m) && (h[y + 1].x > h[y].x)) y = y + 1;
    h[0] = h[x];
    h[x] = h[y];
    h[y] = h[0];
    x = y;
  }
}
void up(int x) {
  int y;
  while ((x > 1) && (h[x / 2].x < h[x].x)) {
    y = x / 2;
    h[0] = h[x];
    h[x] = h[y];
    h[y] = h[0];
    x = y;
  }
}
int main() {
  cin >> n >> s;
  m = 0;
  for (int i = 1; i <= n; i++) {
    m = m + 1;
    cin >> h[m].x;
    if (h[m].x != 0) {
      h[m].y = i;
      up(m);
    } else
      m = m - 1;
  }
  while (m > 0) {
    if (h[1].x > (m - 1)) {
      cout << "No";
      return 0;
    }
    t = h[1];
    h[1] = h[m];
    m = m - 1;
    down(1);
    for (int i = 1; i <= t.x; i++) {
      a[i] = h[1];
      h[1] = h[m];
      m = m - 1;
      down(1);
    }
    for (int i = 1; i <= t.x; i++) {
      len = len + 1;
      ans[len].x = t.y;
      ans[len].y = a[i].y;
      a[i].x = a[i].x - 1;
      if (a[i].x != 0) {
        m = m + 1;
        h[m] = a[i];
        up(m);
      }
    }
  }
  cout << "Yes" << endl << len << endl;
  for (int i = 1; i <= len; i++) cout << ans[i].x << " " << ans[i].y << endl;
  return 0;
}
