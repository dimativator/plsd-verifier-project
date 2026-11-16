#include <bits/stdc++.h>
using namespace std;
int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);
  int t;
  scanf("%d", &t);
  while (t--) {
    vector<pair<long long, long long> > v, v1;
    int n, x, y;
    long long a, b, mn = 1000000000000, mn1 = 1000000000000, ans = 0, ans1 = 0,
                    res = 0;
    scanf("%d", &n);
    x = n, y = n;
    for (int i = 0; i < n; i++) {
      scanf("%lld %lld", &a, &b);
      v.push_back(make_pair(a, b));
      v1.push_back(make_pair(a, b));
      if (a < mn) {
        mn = a;
        x = i;
      }
    }
    for (int i = 0; i < n - 1; i++) {
      if (v[i + 1].first - v[i].second > 0) {
        if (mn1 > v[i].second) {
          mn1 = v[i].second;
          y = i + 1;
        }
      }
    }
    if (v[0].first - v[n - 1].second > 0) {
      if (mn1 > v[n - 1].second) {
        mn1 = v[n - 1].second;
        y = 0;
      }
    }
    for (int i = x; i < n; i++) {
      ans += v[i].first;
      if (i == n - 1) {
        v[0].first -= v[i].second;
        if (v[0].first < 0) {
          v[0].first = 0;
        }
      } else {
        v[i + 1].first -= v[i].second;
        if (v[i + 1].first < 0) {
          v[i + 1].first = 0;
        }
      }
    }
    for (int i = 0; i < x; i++) {
      ans += v[i].first;
      if (i + 1 < x) {
        v[i + 1].first -= v[i].second;
        if (v[i + 1].first < 0) {
          v[i + 1].first = 0;
        }
      }
    }
    for (int i = y; i < n; i++) {
      ans1 += v1[i].first;
      if (i == n - 1) {
        v1[0].first -= v1[i].second;
        if (v1[0].first < 0) {
          v1[0].first = 0;
        }
      } else {
        v1[i + 1].first -= v1[i].second;
        if (v1[i + 1].first < 0) {
          v1[i + 1].first = 0;
        }
      }
    }
    for (int i = 0; i < y; i++) {
      ans1 += v1[i].first;
      if (i + 1 < y) {
        v1[i + 1].first -= v1[i].second;
        if (v1[i + 1].first < 0) {
          v1[i + 1].first = 0;
        }
      }
    }
    res = min(ans, ans1);
    printf("%lld\n", res);
  }
  return 0;
}
