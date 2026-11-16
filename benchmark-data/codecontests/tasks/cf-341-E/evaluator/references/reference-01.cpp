#include <bits/stdc++.h>
using namespace std;
template <class T>
inline void read(T &x) {
  x = 0;
  char c = getchar();
  int f = 1;
  while (!isdigit(c)) {
    if (c == '-') f = -1;
    c = getchar();
  }
  while (isdigit(c)) {
    x = x * 10 + c - '0';
    c = getchar();
  }
  x *= f;
}
template <class T>
inline void umin(T &x, T y) {
  x = x < y ? x : y;
}
template <class T>
inline void umax(T &x, T y) {
  x = x > y ? x : y;
}
inline unsigned int R() {
  static unsigned int seed = 416;
  return seed ^= seed >> 5, seed ^= seed << 17, seed ^= seed >> 13;
}
const int N = 2666;
int n, a[N];
pair<int, int> ans[1766666];
int tot;
int sta[N], top;
void move(int i, int j) {
  ans[++tot] = pair<int, int>(i, j);
  assert(a[i] <= a[j]);
  a[j] -= a[i];
  a[i] += a[i];
}
void solve(int x, int y, int z) {
  if (a[y] > a[z]) swap(y, z);
  if (a[x] > a[y]) swap(x, y);
  if (a[y] > a[z]) swap(y, z);
  assert(a[x] <= a[y] && a[y] <= a[z]);
  if (!a[x]) return;
  if (a[y] % a[x] <= a[x] / 2) {
    int k = a[y] / a[x], cur = 1;
    while (k) {
      if (k & cur)
        k ^= cur, move(x, y);
      else
        move(x, z);
      cur <<= 1;
    }
  } else {
    int k = a[y] / a[x] + 1, mi = 1;
    while (mi * 2 <= k) mi *= 2;
    int tmp = k - mi;
    for (int c = 1; c * 2 <= mi; c *= 2) {
      if (tmp & c)
        tmp ^= c, move(x, y);
      else
        move(x, z);
    }
    move(y, x);
  }
  solve(x, y, z);
}
int main() {
  read(n);
  for (register int i = (1); i <= (n); i++) read(a[i]);
  for (register int i = (1); i <= (n); i++)
    if (a[i]) sta[++top] = i;
  if (top <= 1) {
    puts("-1");
    return 0;
  }
  while (top >= 3) {
    int x = sta[top--], y = sta[top--], z = sta[top--];
    solve(x, y, z);
    if (a[x]) sta[++top] = x;
    if (a[y]) sta[++top] = y;
    if (a[z]) sta[++top] = z;
  }
  printf("%d\n", tot);
  for (register int i = (1); i <= (tot); i++)
    printf("%d %d\n", ans[i].first, ans[i].second);
  int cnt = 0;
  for (register int i = (1); i <= (n); i++) cnt += a[i] > 0;
  assert(cnt == 2);
  return 0;
}
