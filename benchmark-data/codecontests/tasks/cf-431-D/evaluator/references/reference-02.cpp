#include <bits/stdc++.h>
using namespace std;
template <typename T>
inline T sqr(T x) {
  return x * x;
}
template <typename T>
inline T getNext() {
  T s = 1, x = 0, c = getc(stdin);
  while (c <= 32) c = getc(stdin);
  if (c == '-') s = -1, c = getc(stdin);
  while ('0' <= c && c <= '9') x = x * 10 + c - '0', c = getc(stdin);
  return x * s;
}
long long m;
int k;
long long d[2][70][70];
int a[70], sz;
long long getMid(long long l, long long r) { return l + (r - l) / 2; }
long long go(bool sp, int p, int o) {
  if (p == sz) {
    return o == k;
  }
  long long &res = d[sp][p][o];
  if (~res) {
    return res;
  }
  res = 0;
  if (sp) {
    for (int i = 0; i != a[p] + 1; i += 1) res += go(a[p] == i, p + 1, o + i);
  } else {
    for (int i = 0; i != 2; i += 1) res += go(0, p + 1, o + i);
  }
  return res;
}
long long calc(long long x) {
  if (!x) return 0;
  sz = 0;
  while (x > 0) {
    a[sz++] = x % 2ll;
    x /= 2;
  }
  memset(d, 255, sizeof d);
  reverse(a, a + sz);
  return go(1, 0, 0);
}
long long get(long long x) { return calc(x + x) - calc(x); }
int main() {
  m = getNext<long long>();
  k = getNext<int>();
  if (m == k && m == 1) {
    puts("1");
    return 0;
  }
  long long l = 1, r = 1000000000000000000ll;
  while (l < r) {
    long long mid = getMid(l, r);
    if (l + 1 == r) break;
    if (get(mid) <= m) {
      l = mid;
    } else {
      r = mid;
    }
  }
  printf("%I64d", l);
  return 0;
}
