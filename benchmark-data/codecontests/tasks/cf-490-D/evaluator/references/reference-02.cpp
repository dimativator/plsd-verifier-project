#include <bits/stdc++.h>
using namespace std;
typedef pair<pair<pair<long long, long long>, pair<long long, long long> >, int>
    point;
map<pair<pair<long long, long long>, pair<long long, long long> >, int> fre;
point res;
int u, v, x, y;
point BFS(point a) {
  queue<point> Q;
  Q.push(a);
  while (!Q.empty()) {
    a = Q.front();
    Q.pop();
    if (fre[make_pair(make_pair(a.first.first.first, a.first.first.second),
                      make_pair(a.first.second.first, a.first.second.second))])
      continue;
    fre[make_pair(make_pair(a.first.first.first, a.first.first.second),
                  make_pair(a.first.second.first, a.first.second.second))] = 1;
    if (a.first.first.first * a.first.first.second ==
        a.first.second.first * a.first.second.second)
      return a;
    if (a.first.first.first * a.first.first.second >
        a.first.second.first * a.first.second.second) {
      if (!(a.first.first.first % 2))
        Q.push(make_pair(
            make_pair(make_pair(a.first.first.first / 2, a.first.first.second),
                      make_pair(a.first.second.first, a.first.second.second)),
            a.second + 1));
      else if (!(a.first.first.second % 2))
        Q.push(make_pair(
            make_pair(make_pair(a.first.first.first, a.first.first.second / 2),
                      make_pair(a.first.second.first, a.first.second.second)),
            a.second + 1));
      if (!(a.first.first.first % 3))
        Q.push(make_pair(
            make_pair(
                make_pair(2 * a.first.first.first / 3, a.first.first.second),
                make_pair(a.first.second.first, a.first.second.second)),
            a.second + 1));
      else if (!(a.first.first.second % 3))
        Q.push(make_pair(
            make_pair(
                make_pair(a.first.first.first, 2 * a.first.first.second / 3),
                make_pair(a.first.second.first, a.first.second.second)),
            a.second + 1));
    } else {
      if (!(a.first.second.first % 2))
        Q.push(make_pair(
            make_pair(
                make_pair(a.first.first.first, a.first.first.second),
                make_pair(a.first.second.first / 2, a.first.second.second)),
            a.second + 1));
      else if (!(a.first.second.second % 2))
        Q.push(make_pair(
            make_pair(
                make_pair(a.first.first.first, a.first.first.second),
                make_pair(a.first.second.first, a.first.second.second / 2)),
            a.second + 1));
      if (!(a.first.second.first % 3))
        Q.push(make_pair(
            make_pair(
                make_pair(a.first.first.first, a.first.first.second),
                make_pair(2 * a.first.second.first / 3, a.first.second.second)),
            a.second + 1));
      else if (!(a.first.second.second % 3))
        Q.push(make_pair(
            make_pair(
                make_pair(a.first.first.first, a.first.first.second),
                make_pair(a.first.second.first, 2 * a.first.second.second / 3)),
            a.second + 1));
    }
  }
  return make_pair(make_pair(make_pair(0, 0), make_pair(0, 0)), -1);
}
int check(long long a, long long b) {
  while (!(a % 2)) a /= 2;
  while (!(a % 3)) a /= 3;
  while (!(b % 2)) b /= 2;
  while (!(b % 3)) b /= 3;
  return a == b;
}
int main() {
  scanf("%d%d%d%d", &x, &y, &u, &v);
  res = BFS(make_pair(make_pair(make_pair(x, y), make_pair(u, v)), 0));
  if (res.second == -1)
    printf("%d", -1);
  else
    printf("%d\n%lld %lld\n%lld %lld", res.second, res.first.first.first,
           res.first.first.second, res.first.second.first,
           res.first.second.second);
}
