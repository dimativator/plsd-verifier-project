#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, m;
  cin >> n >> m;
  vector<pair<int, int> > a;
  a.push_back(make_pair(0, 0));
  if (n > 0) a.push_back(make_pair(1, 0));
  if (m > 0) a.push_back(make_pair(0, 1));
  if (n > 0 && m > 0) a.push_back(make_pair(1, 1));
  a.push_back(make_pair(n, m));
  if (n > 0) a.push_back(make_pair(n - 1, m));
  if (m > 0) a.push_back(make_pair(n, m - 1));
  if (n > 0 && m > 0) a.push_back(make_pair(n - 1, m - 1));
  a.push_back(make_pair(n, 0));
  if (n > 0) a.push_back(make_pair(n - 1, 0));
  if (m > 0) a.push_back(make_pair(n, 1));
  if (n > 0 && m > 0) a.push_back(make_pair(n - 1, 1));
  a.push_back(make_pair(0, m));
  if (n > 0) a.push_back(make_pair(1, m));
  if (m > 0) a.push_back(make_pair(0, m - 1));
  if (n > 0 && m > 0) a.push_back(make_pair(1, m - 1));
  long double d = 0;
  vector<int> ans(4);
  for (int i1 = 0; i1 < a.size(); i1++)
    for (int i2 = 0; i2 < a.size(); i2++)
      for (int i3 = 0; i3 < a.size(); i3++)
        for (int i4 = 0; i4 < a.size(); i4++) {
          long double dd = 0;
          dd += sqrt((a[i1].first - a[i2].first) * (a[i1].first - a[i2].first) +
                     (a[i1].second - a[i2].second) *
                         (a[i1].second - a[i2].second));
          dd += sqrt((a[i2].first - a[i3].first) * (a[i2].first - a[i3].first) +
                     (a[i2].second - a[i3].second) *
                         (a[i2].second - a[i3].second));
          dd += sqrt((a[i3].first - a[i4].first) * (a[i3].first - a[i4].first) +
                     (a[i3].second - a[i4].second) *
                         (a[i3].second - a[i4].second));
          if (dd > d && (a[i1] != a[i2]) && (a[i1] != a[i3]) &&
              (a[i1] != a[i4]) && (a[i2] != a[i3]) && (a[i2] != a[i4]) &&
              (a[i3] != a[i4])) {
            ans[0] = i1, ans[1] = i2, ans[2] = i3, ans[3] = i4;
            d = dd;
          }
        }
  cout << a[ans[0]].first << ' ' << a[ans[0]].second << endl;
  cout << a[ans[1]].first << ' ' << a[ans[1]].second << endl;
  cout << a[ans[2]].first << ' ' << a[ans[2]].second << endl;
  cout << a[ans[3]].first << ' ' << a[ans[3]].second << endl;
  return 0;
}
