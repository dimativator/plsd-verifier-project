#include <bits/stdc++.h>
using namespace std;
int l[100100];
int main() {
  int n, h;
  int ans;
  int id;
  cin >> n >> h;
  vector<pair<int, int> > a;
  a.clear();
  int x;
  for (int i = 0; i < n; i++) {
    cin >> x;
    a.push_back(make_pair(x, i));
  }
  sort(a.begin(), a.end());
  if (a.size() <= 2) {
    cout << 0 << endl;
    for (int i = 0; i < a.size(); i++) {
      if (i) cout << " ";
      cout << 1;
    }
    cout << endl;
  } else {
    ans = 1000000000;
    id = 0;
    ans = a[n - 1].first + a[n - 2].first - a[1].first - a[0].first;
    int arr1[4];
    int arr2[4];
    for (int i = 1; i < a.size(); i++) {
      for (int j = 0; j < 4; j++) arr1[j] = arr2[j] = -1;
      arr1[0] = 1;
      if (i > 1) {
        arr1[1] = 2;
        arr1[2] = i - 1;
        arr1[3] = i;
      } else {
        arr1[1] = 1;
        arr1[2] = 1;
        arr1[3] = 1;
      }
      arr2[0] = 0;
      if (i + 2 < a.size()) {
        arr2[1] = i + 1;
        arr2[2] = n - 2;
        arr2[3] = n - 1;
      } else if (i + 1 < a.size()) {
        arr2[1] = n - 1;
        arr2[2] = n - 1;
        arr2[3] = n - 1;
      } else {
        arr2[1] = 0;
        arr2[2] = 0;
        arr2[3] = 0;
      }
      int max_ = -1;
      int min_ = 1000000000;
      for (int k1 = 0; k1 < 4; k1++) {
        for (int k2 = 0; k2 < 4; k2++) {
          if (arr1[k1] != arr1[k2]) {
            max_ = max(max_, a[arr1[k1]].first + a[arr1[k2]].first);
            min_ = min(min_, a[arr1[k1]].first + a[arr1[k2]].first);
          }
          if (arr2[k1] != arr2[k2]) {
            max_ = max(max_, a[arr2[k1]].first + a[arr2[k2]].first);
            min_ = min(min_, a[arr2[k1]].first + a[arr2[k2]].first);
          }
          max_ = max(max_, a[arr1[k1]].first + a[arr2[k2]].first + h);
          min_ = min(min_, a[arr1[k1]].first + a[arr2[k2]].first + h);
        }
      }
      if (max_ - min_ < ans) {
        ans = max_ - min_;
        id = i;
      }
    }
    cout << ans << endl;
    l[a[0].second] = 2;
    for (int i = 1; i <= id; i++) l[a[i].second] = 1;
    for (int i = id + 1; i < n; i++) l[a[i].second] = 2;
    for (int i = 0; i < n; i++) {
      if (i) cout << " ";
      cout << l[i];
    }
    cout << endl;
  }
  return 0;
}
